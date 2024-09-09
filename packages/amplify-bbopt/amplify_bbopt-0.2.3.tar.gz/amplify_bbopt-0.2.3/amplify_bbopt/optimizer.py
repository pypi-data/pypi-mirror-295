# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

import sys
import time
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Callable, Generic, TypeVar

import amplify
import numpy as np

from .bb_func import BlackBoxFuncBase, BlackBoxFuncList
from .data_list import DataList
from .history import History
from .logger import logger
from .misc import exec_func_neat_stdout, header_obj, long_line, print_to_str
from .model import ModelKernel, QUBOConvertibleBase, TorchFM
from .plot import anneal_history
from .solution_type import FlatSolution, FlatSolutionDict, StructuredSolution, StructuredSolutionDict
from .trainer import ModelKernelTrainer, TorchFMTrainer, TrainerBase


class OptimizerBase(ABC):
    """Base class for black-box optimizer."""

    def __init__(
        self,
        data: DataList,
        objective: BlackBoxFuncBase,
        objective_weight: float | Callable[[Any], float] = 1.0,
    ) -> None:
        """Initialize `OptimizerBase`.

        Args:
            data (DataList): Initial training dataset.
            objective (BlackBoxFuncBase): Objective (black-box) function class instance created with :obj:`blackbox` decorator.
            objective_weight (float | Callable[[int, Any], float], optional): A weight imposed on the objective function in `amplify.Model`. If a Callable object is passed, a weight is the return value of the object with the used optimizer instance as an argument at each optimization cycle. Generally, `weight` is only useful in case of multi-objective optimization using :obj:`MultiObjectiveOptimizer`. Defaults to 1.
        """  # noqa: E501
        self._data = data.copy()
        self._num_initial_data = len(self._data)

        self._objective = objective
        self._objective_weight_f = objective_weight
        self._objective_weight: float | None = None
        self._i_cycle = 0
        self._best_objective: int | float | None = None
        self._best_solution = StructuredSolutionDict()

    @property
    def num_initial_data(self) -> int:
        """A number of the samples in initial data."""
        return self._num_initial_data

    @num_initial_data.setter
    def num_initial_data(self, value: int) -> None:
        """Set a number of the samples in initial data.

        Args:
            value (int): A number of the samples in initial data.
        """
        self._num_initial_data = value

    @property
    def objective(self) -> BlackBoxFuncBase:
        """Objective function class instance."""
        return self._objective

    @property
    def i_cycle(self) -> int:
        """The number of current optimization cycle."""
        return self._i_cycle

    @property
    def objective_weight(self) -> float | None:
        """The latest weight for the objective function."""
        return self._objective_weight

    def update_objective_weight(self, optimizer: Any) -> None:  # noqa: ANN401
        """Update the weight for the objective function.

        The weight is determined according to the weight function passed to :obj:`OptimizerBase.__init__` (:obj:`OptimizerBase.objective_weight` is `callable`). In case of :obj:`OptimizerBase.objective_weight` being `float`, the weight is constant over optimization cycles. Expected to be executed at the beginning of each optmization cycle.

        Args:
            optimizer (Any): An optimizer to be passed to the `callable` :obj:`OptimizerBase.objective_weight`.
        """  # noqa: E501
        if callable(self._objective_weight_f):
            self._objective_weight = self._objective_weight_f(optimizer)
        else:
            self._objective_weight = self._objective_weight_f

    @property
    def best_objective(self) -> int | float:
        """Objective function value corresponding to the current best solution (optimaized input)."""
        assert self._best_objective is not None
        return self._best_objective

    @property
    def best_solution(self) -> StructuredSolutionDict:
        """Current best solution (optimized input)."""
        return self._best_solution

    def set_best(self, best_solution_dict: FlatSolutionDict | None = None) -> None:
        """Set the current best solution and corresponding objective function value.

        Args:
            best_solution_dict (FlatSolutionDict | None, optional): A solution dictionary. This may contains solution values from other objective functions in case of multiple-objective optimization. In this case, 'best' means the variable value vector relevant to an individual objective function, that is a subset of the entire solution which achieve the best of multiple-objectives combined. Therefore, the set best here may not be the same as the best in `OptimizerBase.data`. If `None` is specified, search the best from `OptimizerBase.data`. Defaults to `None`.
        """  # noqa: E501
        variables = self._objective.variables
        if best_solution_dict is None:
            self._best_objective = np.array(self._data.y).min()
            self._best_solution = (
                FlatSolution(variables, self._data.x[np.array(self._data.y).argmin()])
                .to_structured()
                .to_solution_dict()
            )
        else:
            self._best_solution = best_solution_dict.to_solution(variables).to_structured().to_solution_dict()
            i = np.array([self._data.x[i] == self._best_solution for i in range(len(self._data.x))]).argmax()
            self._best_objective = np.array(self._data.y)[i]

    @property
    def data(self) -> DataList:
        """Current training dataset (both input and output of an individual objective function)."""
        return self._data

    def fetch_history(self) -> History:
        """Return the optimization history.

        Returns:
            History: The optimization history.
        """
        return History(self._data)

    @abstractmethod
    def optimize(self) -> None:
        """A method to execute optimization."""


T = TypeVar("T", bound=TrainerBase)  # for trainer class
M = TypeVar("M", bound=QUBOConvertibleBase)  # for model class


class QAOptimizerBase(OptimizerBase, Generic[T, M]):
    """Base class for black-box optimizater based on (quantum) annealing of a surrogate/acquisition model.

    - :obj:`T` = :obj:`TypeVar` (:obj:`T`, bound= :obj:`TrainerBase`)
    - :obj:`M` = :obj:`TypeVar` (:obj:`M`, bound= :obj:`QUBOConvertibleBase`)

    """

    def __init__(
        self,
        data: DataList,
        objective: BlackBoxFuncBase,
        client: (
            amplify.FixstarsClient
            | amplify.DWaveSamplerClient
            | amplify.LeapHybridSamplerClient
            | amplify.LeapHybridCQMSamplerClient
            | amplify.FujitsuDA4Client
            | amplify.ToshibaSQBM2Client
            | amplify.GurobiClient
            | amplify.NECVA2Client  # as of v1.1.0
        )
        | None,
        trainer_class: type[T],
        seed: int = 0,
        objective_weight: float | Callable[[Any], float] = 1.0,
    ) -> None:
        """Initialize QA-based optimizer.

        Args:
            data (DataList): Initial training dataset.
            objective (BlackBoxFuncBase): A black-box function class instance created with :obj:`blackbox` decorator.
            client (amplify.FixstarsClient  |  amplify.DWaveSamplerClient  |  amplify.LeapHybridSamplerClient  |  amplify.LeapHybridCQMSamplerClient  |  amplify.FujitsuDA4Client  |  amplify.ToshibaSQBM2Client  |  amplify.GurobiClient  |  amplify.NECVA2Client): A solver client available in the Amplify SDK.
            trainer_class (Type[T]): A trainer class for a surrogate/acquisition model.
            seed (int, optional): A random seed. Defaults to 0.
            objective_weight (float | Callable[[Any], float], optional): A weight imposed on the objective function in `amplify.Model`. If a Callable object is passed, a weight is the return value of the object with the used optimizer instance as an argument at each optimization cycle. Generally, `weight` is only useful in case of multi-objective optimization using :obj:`MultiObjectiveOptimizer`. Defaults to 1.0.
        """  # noqa: E501
        super().__init__(data, objective, objective_weight)
        assert self.objective.variables.poly_array is not None

        self._client = client
        self.constraints = objective.constraints
        self._trainer = trainer_class()

        self._seed = seed
        self._rng = np.random.default_rng(self._seed)
        self._surrogate_model: M | None = None

        self._amplify_model: amplify.Model | None = None
        self._custom_amplify_objective: amplify.Poly | None = None
        self._duplicate_solution_counter: dict[tuple, int] = {}

        self._solution_frequency = self.SolutionFrequency(counter_threshold=10)

        self._target_num_iterations: int | None = None

        self._elapsed_time: list[float] = [0.0] * len(self._data)
        self._is_de_duplication: list[bool] = [True] * len(self._data)

    class SolutionFrequency:
        """Class to determine whether a given solution appears frequently or not."""

        def __init__(self, counter_threshold: int) -> None:
            self._solution_counter: dict[tuple, int] = {}
            self._counter_threshold = counter_threshold

        def _update_item(self, input_dict: dict[tuple, int]) -> dict[tuple, int]:
            """Items with values between 0 and 2*counter_threshold stay in the dict.

            Returns:
                dict[tuple, int]: The updated item dict.

            """
            return {
                key: value for key, value in input_dict.items() if value >= 0 and value <= 2 * self._counter_threshold
            }

        def _update_counter(self, sol_key: tuple) -> None:
            """For the current solution, +1. Other solutions -1.

            Solutions with a -ve count will be removed from the dict
            """
            if sol_key not in self._solution_counter:
                self._solution_counter[sol_key] = 0
            for sol in self._solution_counter:
                self._solution_counter[sol] -= 1
            self._solution_counter[sol_key] += 2
            self._solution_counter = self._update_item(self._solution_counter)

        def is_frequent(self, solution: FlatSolutionDict) -> bool:
            sol_key = tuple(solution.to_list())
            self._update_counter(sol_key)
            return sol_key in self._solution_counter and self._solution_counter[sol_key] > self._counter_threshold

        def how_frequent(self, solution: FlatSolutionDict) -> int:
            sol_key = tuple(solution.to_list())
            self._update_counter(sol_key)
            if sol_key in self._solution_counter:
                return self._solution_counter[sol_key]
            return 0

    def set_best(self, best_solution_dict: FlatSolutionDict | None = None) -> None:
        """Set the current best solution and corresponding objective function value.

        If :obj:`QAOptimizerBase.custom_amplify_objective` is set, the :obj:`QAOptimizerBase.best_objective` include the value of the custom objective as well. This inclusion of the custom objective is the difference from :obj:`OptimizerBase.set_best`.

        Args:
            best_solution_dict (FlatSolutionDict | None, optional): A solution dictionary. This may contains solution values from other objective functions in case of multiple-objective optimization. In this case, 'best' means the variable value vector relevant to an individual objective function, that is a subset of the entire solution which achieve the best of multiple objectives combined. Therefore, the set best here may not be the same as the best in `QAOptimizerBase.data`. If `None` is specified, search the best from `OptimizerBase.data`. Defaults to `None`.
        """  # noqa: E501
        variables = self._objective.variables
        if best_solution_dict is None:
            self._best_objective = sys.float_info.max
            for x, y in self._data:
                assert y is not None
                solution = FlatSolution(variables, x).to_structured()
                # custom objective (self._evaluate_custom_objective returns 0 if no custom obj is set)
                y_custom_obj = self._evaluate_custom_objective(solution)
                y_total = y_custom_obj + y
                if y_total < self._best_objective:
                    self._best_objective = y_total
                    self._best_solution = solution.to_solution_dict()
        else:
            self._best_solution = best_solution_dict.to_solution(variables).to_structured().to_solution_dict()
            i = np.array([self._data.x[i] == self._best_solution for i in range(len(self._data.x))]).argmax()
            self._best_objective = np.array(self._data.y)[i]
            # custom objective (self._evaluate_custom_objective returns 0 if no custom obj is set)
            assert self._best_objective is not None
            self._best_objective += self._evaluate_custom_objective(self._best_solution.to_solution(variables))

    @property
    def custom_amplify_objective(self) -> amplify.Poly | None:
        """Custom objective function that may be ceated directly from `amplify.PolyArray`.

        Custom objective does NOT have to be converted from the surrogate model of the black-box function. Retieve `amplify.PolyArray` via :obj:`Variables.poly_array` or :obj:`Variables.amplify_variables`, and construct an Amplify SDK's objective function directly, which will be added to the objective constructed from a surrogate model while creating `amplify.Model`. Such a custom objective function must be created after the instantiation of an QA-based optimizer class, as this is when `amplify.PolyArray`'s are issued for each of the variables.


        Returns:
            amplify.Poly | None: Custom objective function.
        """  # noqa: E501
        return self._custom_amplify_objective

    @custom_amplify_objective.setter
    def custom_amplify_objective(self, value: amplify.Poly | None) -> None:
        self._custom_amplify_objective = value

    def __str__(self) -> str:
        """Some human-readable information relevant to the optimizer.

        Returns:
            str: Description.
        """
        variables = self._objective.variables
        ret = print_to_str(f"num variables: {len(variables)}")
        ret += print_to_str(f"num elemental variables: {variables.num_elemental_variables}")
        ret += print_to_str(f"num amplify variables: {variables.num_amplify_variables}")
        ret += print_to_str(f"optimizer client: {type(self._client).__name__}")
        if callable(self._objective_weight_f):
            ret += print_to_str(f"objective weight: {self._objective_weight_f.__name__}")
        else:
            ret += print_to_str(f"objective weight: {self._objective_weight_f}")
        if len(self.constraints) > 0:
            ret += print_to_str(f"{self.constraints}")
        ret += print_to_str(self._trainer)
        return ret

    @property
    def surrogate_model(self) -> M | None:
        """The current surrogate model. If not set return `None`.

        Returns:
            M | None:
        """
        return self._surrogate_model

    @property
    def amplify_model(self) -> amplify.Model | None:
        """The current Amplify-SDK model. If the model is not constructed yet, return `None`.

        Returns:
            amplify.Model | None:
        """
        return self._amplify_model

    @property
    def trainer(self) -> T:
        """The instance of the trainer class."""
        return self._trainer

    def _evaluate_objective_func(self, solution: StructuredSolution) -> float:
        """Evaluate the black-box objective function with a solution.

        Args:
            solution (StructuredSolution): A solution.

        Returns:
            tuple[float, float | None]: The return values from (first) the black-box objective function and (second) the value of custom objective (:obj:`QAOptimizerBase.custom_amplify_objective`). The second is None if no custom objective is set.
        """  # noqa: E501
        inp = solution.to_solution_dict()
        return exec_func_neat_stdout(header_obj, self._objective._call_objective, logger(), **inp)  # type: ignore # noqa: SLF001

    def _evaluate_custom_objective(self, solution: StructuredSolution) -> float:
        """Evaluate the custom Amplify-SDK compatible objective. If no custom objective is set return 0.

        Args:
            solution (StructuredSolution): The Amplify BBOpt's solution.

        Returns:
            float: The evaluation result. If no custom objective is set return 0.
        """
        if self._custom_amplify_objective is None:
            return 0.0
        amplify_solution_dict = self.objective.variables.convert_to_amplify_solution_dict(solution.to_solution_dict())
        return float(self._custom_amplify_objective.substitute(amplify_solution_dict))  # type: ignore

    def optimize(
        self,
        num_cycles: int = 10,
        constraint_weight: float | None = None,
        num_solves: int = 1,
        search_max: int = 1000,
        show_annealing_history: bool = False,
        target_num_iterations: int | None = None,
    ) -> None:
        """A function to execute black-box optmization with FMQA.

        Args:
            num_cycles (int, optional): A number of optimization iterations. Defaults to 10.
            constraint_weight (float | None, optional): A weight for constraints. If set `None`, the weight is determined based on the latest training data as in 2 times of :obj:`DataList.abs_y_max`. If constraint weights are seperately set for :obj:`Constraint.weight`, this `constraint_weight` is multiplied on top of :obj:`Constraint.weight`. Defaults to `None`.
            num_solves (int, optional): A number of serial solver execution in the Amplify SDK's serial solver execution (https://amplify.fixstars.com/en/docs/amplify/v1/serial.html). Defaults to 1.
            search_max (int, optional): If the found solution is found the training data, alternative solution close to the original solution is searched for at most `search_max` times. Defaults to 1000.
            show_annealing_history (bool, optional): True to show a annealing history with time stamp. Available when Amplify Annealing Engine (`amplify.FixstarsClient`) is specified as the client in the constructor. Defaults to False.
            target_num_iterations (int | None, optional): Annealing timeout is controlled based on the [previous timeout] * target_num_iterations / [previous num_iterations]. Available when Amplify Annealng Engine is used for optimization solver. Set `None` to use the given timeout constantly. Defaults to None.
        """  # noqa: E501
        if show_annealing_history and isinstance(self._client, amplify.FixstarsClient):
            self._client.parameters.outputs.num_outputs = 0  # return all the found solutions

        self._target_num_iterations = target_num_iterations

        self._trainer.init_seed(self._seed)

        start = time.perf_counter()

        for self._i_cycle in range(num_cycles):
            weight = 2.0 * self._data.abs_y_max if constraint_weight is None else constraint_weight

            logger().info(long_line)
            logger().info(f"#{self._i_cycle + 1}/{num_cycles} optimization cycle, constraint wt: {weight:.2e}")
            # Prepare
            variables = self._objective.variables
            x_list_structured = self._data.to_structured_solution_list(variables)
            x_list_encoded = [variables.encode(x_list_structured[i]) for i in range(len(self._data))]
            # Perform FMQA
            self._surrogate_model = self._trainer.train(x_list_encoded, self._data.y, logger())
            self._amplify_model = self._generate_amplify_model(self._surrogate_model, weight)  # type: ignore
            x_hat = self._anneal(self._amplify_model, num_solves, show_annealing_history)
            x_hat_unique, is_modified = self._ensure_uniqueness(x_hat, search_max)
            # Evaluate black-box function and store the new input-output sample
            y_hat = self._evaluate_objective_func(x_hat_unique)
            y_custom = self._evaluate_custom_objective(x_hat_unique)
            self._data.append((x_hat_unique.to_flat().values, y_hat))
            self._data.save()
            self.set_best()
            if self._custom_amplify_objective is None:
                logger().info(f"{y_hat=:.3e}, best objective={self.best_objective:.3e}")
            else:
                assert y_custom is not None
                logger().info(f"{y_hat=:.3e}, {y_custom=:.3e}, best objective={self.best_objective:.3e}")

            self._elapsed_time.append(time.perf_counter() - start)
            self._is_de_duplication.append(is_modified)

    def _generate_amplify_model(
        self,
        model: M,
        constraint_weight: float = 1.0,
        external_optimizer: Any | None = None,  # noqa: ANN401
    ) -> amplify.Model:
        """Generate the Amplify SDK model from a trained surrogate/acquisition model.

        The user defined `objective_weight` function specified in :obj:`FMQAOptimizer.__init__` is multiplied to the `amplify.Model.objective` here.

        Args:
            model (M): A trained surrogate/acquisition model.
            constraint_weight (float, optional): A weight for constraints. Defaults to 1.0.
            external_optimizer(Any | None, optional): An optimizer. If an external optimizer perform the optimization while using methods in :obj:`FMQAOptimizer`, pass the external optimizer here. This optimizer will be pass to the user defined `objective_weight` function specified in :obj:`FMQAOptimizer.__init__`. If `None` is set, the current instance of :obj:`FMQAOptimizer` is passed. Defaults to `None`.

        Returns:
            amplify.Model: The generated Amplify SDK model.
        """  # noqa: E501
        if external_optimizer is None:
            self.update_objective_weight(self)
        else:
            self.update_objective_weight(external_optimizer)

        variables = self._objective.variables
        objective = model.to_qubo(variables.poly_array)
        constraints = variables.generate_amplify_constraint() + self.constraints.to_amplify_constraint()
        assert self._objective_weight is not None
        if self._custom_amplify_objective is not None:
            objective += self._custom_amplify_objective
        return amplify.Model(self._objective_weight * objective, constraint_weight * constraints)

    def _anneal(
        self, model: amplify.Model, num_solves: int = 1, show_annealing_history: bool = False
    ) -> StructuredSolution:
        """Perform annealing for the constructed `amplify.Model` with constraints.

        Args:
            model (amplify.Model): An Amplify-SDK model (`amplify.Model`).
            num_solves (int, optional): A number of serial solver execution in the Amplify SDK's serial solver execution (https://amplify.fixstars.com/en/docs/amplify/v1/serial.html). Defaults to 1.
            show_annealing_history (bool, optional): True to show a annealing history with time stamp. Available when Amplify Annealing Engine (`amplify.FixstarsClient`) is specified as the client in the constructor. Defaults to False.

        Raises:
            ValueError: If a solver client is not set.
            RuntimeError: If no solution is found.

        Returns:
            StructuredSolution: A solution vector.
        """  # noqa: E501
        if self._client is None:
            raise ValueError("Solver client must be specified.")

        result = amplify.solve(model, self._client, num_solves=num_solves)

        if len(result.solutions) > 0:
            if isinstance(result.client_result, amplify.FixstarsClient.Result):
                num_iterations = result.client_result.execution_parameters.num_iterations
                logger().info(f"num_iterations: {num_iterations}")
                if self._target_num_iterations is not None:
                    next_timeout_ms = (
                        self._target_num_iterations
                        / num_iterations
                        * self._client.parameters.timeout.total_seconds()  # type: ignore
                        * 1000
                    )
                    logger().info(f"timeout updated to: {int(next_timeout_ms)} ms")
                    self._client.parameters.timeout = timedelta(milliseconds=int(next_timeout_ms))  # type: ignore
                if show_annealing_history:
                    anneal_hist = anneal_history(result)
                    if anneal_hist is not None:
                        anneal_hist.show()
            variables = self._objective.variables
            q = variables.poly_array
            return variables.decode(q.evaluate(result.best.values).tolist())
        raise RuntimeError("No solution was found.")

    def _generate_alternative_solution(
        self, solution: StructuredSolution | None, search_count_max: int, find_neighbour: bool = False
    ) -> StructuredSolution:
        """Generate a solution that is close to the original solution. The new solution also meets the user defined constraints when a sufficient search_count_max is given.

        Args:
            solution (StructuredSolution | None): The original solution. If set `None`, alternative solution is randomly generated and it is likely not close to the original solution.
            search_count_max (int): Alternative solution close to the original solution is searched for at most `search_count_max` times.
            find_neighbour (bool, optional): True to generate a random value neighbour to the reference value. Defaults to `False`.

        Returns:
            StructuredSolution: The (updated)) solution.
        """  # noqa: E501
        for _ in range(search_count_max):
            solution_new = self._objective.variables.generate_random_value(self._rng, solution, find_neighbour)
            if self.constraints.is_satisfied(solution_new.to_flat().to_solution_dict()):
                return solution_new
        logger().warning("No alternative solution was found that meets the constraints. The original solution is used.")
        assert solution is not None
        return solution

    def _ensure_uniqueness(
        self, solution: StructuredSolution, search_count_max: int
    ) -> tuple[StructuredSolution, bool]:
        """Ensure the uniqueness of the found solution.

        If the solution is not unique, return a randomly generated solution that is close to the original solution. This new solution should satisfy all the variable-related and user-defined constraints. the search is performed for the maximum of search_count_max times. If no unique and alternative solution is found, return the original solution.

        Args:
            solution (StructuredSolution): A solution.
            search_count_max (int): Alternative solution close to the original solution is searched for at most `search_count_max` times.

        Returns:
            tuple[StructuredSolution, bool]: The (updated) solution and whether the retuend solution is (randomly) modified solution.
        """  # noqa: E501
        original_solution = solution

        is_frequent = self._solution_frequency.is_frequent(solution.to_flat().to_solution_dict())

        how_frequent = self._solution_frequency.how_frequent(solution.to_flat().to_solution_dict())

        for i in range(search_count_max):
            if self.data.is_unique(solution.to_flat().to_solution_dict()):
                if original_solution.values != solution.values:
                    logger().info(
                        f"modifying solution ({i}, {is_frequent=}), "
                        f"{original_solution.to_solution_dict()} --> {solution.to_solution_dict()}.",
                    )
                return solution, i != 0

            if is_frequent:
                # if the same solution appears "frequently", alternative solution is made such that
                # the new solution is close (in the below two levels) to the original solution.
                if how_frequent % 2 == 0:
                    solution = self._generate_alternative_solution(solution, search_count_max, find_neighbour=True)
                else:
                    solution = self._generate_alternative_solution(solution, search_count_max)
            else:
                # If the same solution appears not too often, generate an alternative solution randomly.
                # If the same solution appears too often, SolutionFrequency returns is_frequent=False.
                # This is because such solution is perhaps the result of optimizer being trapped in a local minimum.
                # Thus, and alternative solution is generated randomly.
                solution = self._generate_alternative_solution(None, search_count_max)

        return original_solution, False

    def fetch_history(self) -> History:
        """Return the optimization history.

        Returns:
            History: The optimization history.
        """
        custom_obj: list[float] = []
        for x, y in self._data:
            assert y is not None
            solution = FlatSolution(self._objective.variables, x).to_structured()
            # custom objective (self._evaluate_custom_objective returns 0 if no custom obj is set)
            custom_obj.append(self._evaluate_custom_objective(solution))

        return History(self._data, self._elapsed_time, self._is_de_duplication, custom_obj, self._num_initial_data)


class FMQAOptimizer(QAOptimizerBase):
    """Class for FMQA."""

    def __init__(
        self,
        data: DataList,
        objective: BlackBoxFuncBase,
        client: (
            amplify.FixstarsClient
            | amplify.DWaveSamplerClient
            | amplify.LeapHybridSamplerClient
            | amplify.LeapHybridCQMSamplerClient
            | amplify.FujitsuDA4Client
            | amplify.ToshibaSQBM2Client
            | amplify.GurobiClient
            | amplify.NECVA2Client  # as of v1.1.0
        )
        | None = None,
        trainer_class: type[TorchFMTrainer] = TorchFMTrainer,
        seed: int = 0,
        objective_weight: float | Callable[[Any], float] = 1.0,
    ) -> None:
        """Initialize kernel-QA optimizer.

        By default, the class uses :obj:`ModelKernelTrainer` as a training class, and this training class uses :obj:`ModelKernel` as a default surrogate/acquisition model class.


        Args:
            data (DataList): Initial training dataset.
            objective (BlackBoxFuncBase): A black-box function class instance created with :obj:`blackbox` decorator.
            client (amplify.FixstarsClient  |  amplify.DWaveSamplerClient  |  amplify.LeapHybridSamplerClient  |  amplify.LeapHybridCQMSamplerClient  |  amplify.FujitsuDA4Client  |  amplify.ToshibaSQBM2Client  |  amplify.GurobiClient  |  amplify.NECVA2Client, optional): A solver client. Defaults to None.
            trainer_class (type[TorchFMTrainer], optional): A solver client available in the Amplify SDK. Defaults to TorchFMTrainer.
            seed (int, optional): A random seed. Defaults to 0.
            objective_weight (float | Callable[[Any], float], optional): A weight imposed on the objective function in `amplify.Model`. If a Callable object is passed, a weight is the return value of the object with the used optimizer instance as an argument at each optimization cycle. Generally, `weight` is only useful in case of multi-objective optimization using :obj:`MultiObjectiveOptimizer`. Defaults to 1.0.
        """  # noqa: E501
        super().__init__(data, objective, client, trainer_class, seed, objective_weight)
        if type(self._trainer) is TorchFMTrainer:
            variables = self._objective.variables
            self._trainer.set_model_params(
                d=variables.num_amplify_variables,  # type: ignore
                k=min(10, variables.num_amplify_variables),  # type: ignore
            )

    @property
    def surrogate_model(self) -> TorchFM | None:
        """The current surrogate model (e.g. an instance of :obj:`TorchFM` by default). If not set return `None`."""
        return self._surrogate_model

    @property
    def trainer(self) -> TorchFMTrainer:
        """The instance of the trainer class (e.g. an instance of :obj:`TorchFMTrainer` by default)."""
        return self._trainer


class KernelQAOptimizer(QAOptimizerBase):
    """Class for kernal-QA."""

    def __init__(
        self,
        data: DataList,
        objective: BlackBoxFuncBase,
        client: (
            amplify.FixstarsClient
            | amplify.DWaveSamplerClient
            | amplify.LeapHybridSamplerClient
            | amplify.LeapHybridCQMSamplerClient
            | amplify.FujitsuDA4Client
            | amplify.ToshibaSQBM2Client
            | amplify.GurobiClient
            | amplify.NECVA2Client  # as of v1.1.0
        )
        | None = None,
        trainer_class: type[ModelKernelTrainer] = ModelKernelTrainer,
        seed: int = 0,
        objective_weight: float | Callable[[Any], float] = 1.0,
    ) -> None:
        """Initialize kernel-QA optimizer.

        By default, the class uses :obj:`ModelKernelTrainer` as a training class, and this training class uses :obj:`ModelKernel` as a default surrogate/acquisition model class.

        Args:
            data (DataList): Initial training dataset.
            objective (BlackBoxFuncBase): A black-box function class instance created with :obj:`blackbox` decorator.
            client (amplify.FixstarsClient  |  amplify.DWaveSamplerClient  |  amplify.LeapHybridSamplerClient  |  amplify.LeapHybridCQMSamplerClient  |  amplify.FujitsuDA4Client  |  amplify.ToshibaSQBM2Client  |  amplify.GurobiClient  |  amplify.NECVA2Client, optional): A solver client. Defaults to None.
            trainer_class (Any, optional):  A trainer class for the surrogate/acquisition model based on kernel method. Defaults to :obj:`ModelKernelTrainer`.
            seed (int, optional): A random seed. Defaults to 0.
            objective_weight (float | Callable[[int, Any], float], optional): A weight imposed on the objective function in `amplify.Model`. If a Callable object is passed, a weight is the return value of the object with the used optimizer instance as an argument at each optimization cycle. Generally, `weight` is only useful in case of multi-objective optimization using :obj:`MultiObjectiveOptimizer`. Defaults to 1.0.
        """  # noqa: E501
        super().__init__(data, objective, client, trainer_class, seed, objective_weight)

    @property
    def surrogate_model(self) -> ModelKernel | None:
        """He current surrogate model (e.g. an instance of :obj:`ModelKernel` by default). If not set return `None`."""
        return self._surrogate_model

    @property
    def trainer(self) -> ModelKernelTrainer:
        """The instance of the trainer class (e.g. an instance of :obj:`ModelKernelTrainer` by default)."""
        return self._trainer


class MultiObjectiveOptimizer:
    """Class for black-box optimization with multiple objective functions."""

    def __init__(
        self,
        optimizers: list[QAOptimizerBase],
        # as of v1.1.0
        client: (
            amplify.FixstarsClient
            | amplify.DWaveSamplerClient
            | amplify.LeapHybridSamplerClient
            | amplify.LeapHybridCQMSamplerClient
            | amplify.FujitsuDA4Client
            | amplify.ToshibaSQBM2Client
            | amplify.GurobiClient
            | amplify.NECVA2Client
        ),
        seed: int = 0,
    ) -> None:
        """Initialize `MultiObjectiveOptimizer`.

        Args:
            optimizers (list[QAOptimizerBase]): A list of optimizers each of which is associated with a black-box function, relevant decision variables and constraints. These optimizers do not have to be the same type, e.g. a list like `[FMQAOptimizer, KernelQAOptimizer]` is allowd. Generally, these individual optimizers are used for everything except the amplify.Model construction and communication with an external solver.
            client (amplify.FixstarsClient  |  amplify.DWaveSamplerClient  |  amplify.LeapHybridSamplerClient  |  amplify.LeapHybridCQMSamplerClient  |  amplify.FujitsuDA4Client  |  amplify.ToshibaSQBM2Client  |  amplify.GurobiClient  |  amplify.NECVA2Client): A solver client available in the Amplify SDK.
            seed (int, optional): A random seed. Defaults to 0.
        """  # noqa: E501
        self._optimizers: list[QAOptimizerBase] = optimizers
        self._objectives = BlackBoxFuncList([optz.objective for optz in optimizers], unify_variables=True)

        self._client = client
        self._seed = seed
        self._rng = np.random.default_rng(self._seed)

        self._best_solution_dict = FlatSolutionDict()
        self._best_objective: int | float | None = None
        self._data = DataList(variable_names=self._objectives.variable_names)
        self._amplify_model: amplify.Model | None = None
        self._i_cycle = 0

        self._custom_amplify_objective = amplify.Poly()

        self._elapsed_time: list[float] = []
        self._is_de_duplication: list[bool] = []

    @property
    def custom_amplify_objective(self) -> amplify.Poly:
        """Custom objective function that may be ceated directly from `amplify.PolyArray`.

        Custom objective does NOT have to be converted from the surrogate model of the black-box function. Retieve `amplify.PolyArray` via :obj:`Variables.poly_array` or :obj:`Variables.amplify_variables`, and construct an Amplify SDK's objective function directly, which will be added to the objective constructed from a surrogate model while creating `amplify.Model`. Such a custom objective function must be created after the instantiation of an QA-based optimizer class, as this is when `amplify.PolyArray`'s are issued for each of the variables.
        """  # noqa: E501
        return self._custom_amplify_objective

    @custom_amplify_objective.setter
    def custom_amplify_objective(self, value: amplify.Poly) -> None:
        self._custom_amplify_objective = value

    @property
    def best_objective(self) -> int | float | None:
        """Objective function value corresponding to the current best solution (optimaized input).

        Returns:
            int | float | None: If no data exists, return `None`
        """
        if len(self._data) == 0:
            return None
        return np.array(self._data.y).min()

    @property
    def best_solution(self) -> FlatSolutionDict | None:
        """Current best solution (optimized input)."""
        if len(self._data) == 0:
            return None
        return self._best_solution_dict

    @property
    def optimizers(self) -> list[QAOptimizerBase]:
        """Optimizers passed to the :obj:`MultiObjectiveOptimizer`."""
        return self._optimizers

    @property
    def objectives(self) -> BlackBoxFuncList:
        """Objective functions considered in the :obj:`MultiObjectiveOptimizer`."""
        return self._objectives

    def optimize(
        self,
        num_cycles: int = 10,
        constraint_weight: float | None = None,
        num_solves: int = 1,
        search_max: int = 1000,
        show_annealing_history: bool = False,
    ) -> None:
        """Perform black-box optmization with multiple objective functions.

        Args:
            num_cycles (int, optional): A number of optimization iterations. Defaults to 10.
            constraint_weight (float | None, optional): A weight for constraints. If set `None`, the weight is determined based on the latest training data as in 2 times of :obj:`DataList.abs_y_max`. If constraint weights are seperately set for :obj:`Constraint.weight`, this `constraint_weight` is multiplied on top of :obj:`Constraint.weight`. Defaults to `None`.
            num_solves (int, optional): A number of serial solver execution in the Amplify SDK's serial solver execution (https://amplify.fixstars.com/en/docs/amplify/v1/serial.html). Defaults to 1.
            search_max (int, optional): If the found solution is found the training data, alternative solution close to the original solution is searched for at most `search_max` times. Defaults to 1000.
            show_annealing_history (bool, optional): True to show a annealing history with time stamp. Available when Amplify Annealing Engine (`amplify.FixstarsClient`) is specified as the client in the constructor. Defaults to False.
        """  # noqa: E501
        if show_annealing_history and isinstance(self._client, amplify.FixstarsClient):
            self._client.parameters.outputs.num_outputs = 0  # return all found solutions

        for optz in self._optimizers:
            optz.trainer.init_seed(self._seed)

        start = time.perf_counter()

        for self._i_cycle in range(num_cycles):
            weight = 2.0 * optz.data.abs_y_max if constraint_weight is None else constraint_weight

            logger().info(long_line)
            logger().info(f"#{self._i_cycle + 1}/{num_cycles} optimization cycle, constraint wt: {weight:.2e}")

            for optz in self._optimizers:
                optz._surrogate_model = self._generate_surrogate_models(optz)  # noqa: SLF001
            self._amplify_model = self._generate_amplify_model(weight)

            x_hat_list = self._anneal(self._amplify_model, num_solves)
            x_hat_list_unique, is_modified = self._ensure_uniqueness(x_hat_list, search_max)
            y_hat_total, y_hat_list = self._evaluate_objective_funcs(x_hat_list_unique)
            # self._evaluate_custom_objective returns 0 is no custom obj is set.
            y_hat_total += self._evaluate_custom_objective(x_hat_list_unique)

            solution_dict = self._combine_solutions(x_hat_list_unique)
            assert list(solution_dict.keys()) == self._data.variable_names

            # update best solution/objective
            if len(self._data.y) == 0 or y_hat_total < self._best_objective:  # type: ignore
                self._best_solution_dict.update(solution_dict)
                self._best_objective = y_hat_total
            for optz in self._optimizers:
                optz.set_best(self._best_solution_dict)

            # Add the evaluation results to the data (both individual and overall objectives)
            for i, optz in enumerate(self._optimizers):
                optz.data.append((x_hat_list_unique[i].to_flat().values, y_hat_list[i]))
                optz.data.save()
            self._data.append((solution_dict.to_list(), y_hat_total))
            self._data.save()

            logger().info(f"{y_hat_total=:.3e}, y_best={np.array(self._data.y).min():.3e}")

            self._elapsed_time.append(time.perf_counter() - start)
            self._is_de_duplication.append(is_modified)

    def _generate_surrogate_models(self, optimizer: QAOptimizerBase) -> QUBOConvertibleBase:
        """Train a surrogate/acquisition model for a given black-box function.

        Args:
            optimizer (QAOptimizerBase): An optimizer for whose objective function (:obj:`QAOptimizerBase.objective`) is modelled based on the training data (:obj:`QAOptimizerBase.data`).

        Returns:
            QUBOConvertibleBase: The trained surrogate model.
        """  # noqa: E501
        optz_vars = optimizer.objective.variables
        x_list_encoded = [
            optz_vars.encode(optimizer.data.to_structured_solution(optz_vars, i)) for i in range(len(optimizer.data))
        ]
        return optimizer.trainer.train(x_list_encoded, optimizer.data.y, logger())

    def _generate_amplify_model(self, constraint_weight: float) -> amplify.Model:
        """Generate an Amplify SDK's model combining all relevant surrogate/acquisition models WITH weights specified in each of given optimizers.

        Args:
            constraint_weight (float): A weight for constraints. If constraint weights are seperately set for :obj:`Constraint.weight`, this `constraint_weight` is multiplied on top of :obj:`Constraint.weight`.

        Returns:
            amplify.Model: The Amplify SDK's model.
        """  # noqa: E501
        objective = amplify.Poly()
        constraint = amplify.ConstraintList()
        for optz in self._optimizers:
            assert optz.surrogate_model is not None
            model = optz._generate_amplify_model(optz.surrogate_model, constraint_weight, self)  # noqa: SLF001
            assert isinstance(model.objective, amplify.Poly)
            objective += model.objective
            constraint += model.constraints
        objective += self._custom_amplify_objective
        return amplify.Model(objective, constraint)

    def _evaluate_objective_funcs(self, individual_solutions: list[StructuredSolution]) -> tuple[float, list[float]]:
        """Evaluate all relevant black-box (objective) functions and combine their outputs WITHOUT the objective weights.

        Args:
            individual_solutions (list[StructuredSolution]): A list of solution vectors for individual objectives.

        Returns:
            tuple[float, list[float]]: The evaluation result (the sum of all outputs without considering the objective weights, and list of individual outputs).
        """  # noqa: E501
        y_hat_total = 0.0
        y_hat_list: list[float] = []
        for i, optz in enumerate(self._optimizers):
            name = optz.objective.name
            y_hat = optz._evaluate_objective_func(individual_solutions[i])  # noqa: SLF001
            y_hat_total += y_hat
            y_hat_list.append(y_hat)
            logger().info(f"{name}: {y_hat:.5e} (wt: {optz.objective_weight:.3e})")
        return y_hat_total, y_hat_list

    def _evaluate_custom_objective(self, individual_solutions: list[StructuredSolution]) -> float:
        """Evaluate the custom Amplify-SDK compatible objective. If no custom objective is set return 0.

        Args:
            individual_solutions (list[StructuredSolution]): A list of individual solutions (Amplify BBOpt's solution).

        Returns:
            float: The evaluation result. If no custom objective is set return 0.
        """
        if self._custom_amplify_objective is None:
            return 0.0

        amplify_solution_dict: dict[amplify.Poly, int | float] = {}
        for optz, solution in zip(self._optimizers, individual_solutions):
            amplify_solution_dict.update(
                optz.objective.variables.convert_to_amplify_solution_dict(solution.to_solution_dict())
            )
        return float(self._custom_amplify_objective.substitute(amplify_solution_dict))  # type: ignore

    def _is_satisfied(self, solution_dict: FlatSolutionDict) -> bool:
        """True if the obtained solution satisfies all constraints for all black-box functions.

        Args:
            solution_dict (FlatSolutionDict): A solution combined for solutions of all objectives.

        Returns:
            bool: Whether the solution satisfies the constraints.
        """
        return all(optz.constraints.is_satisfied(solution_dict) for optz in self._optimizers)

    def _generate_alternative_solution(
        self, combined_solution: FlatSolutionDict, search_count_max: int
    ) -> FlatSolutionDict:
        """Generate a solution that is close to the original solution.

        The alternative solution is a unique solution (one not found in the current training dataset) and meets the user-defined constraints when a sufficient search_count_max is given.

        Args:
            combined_solution (FlatSolutionDict): A solution combined for solutions of all objectives.
            search_count_max (int): Alternative solution close to the original solution is searched for at most `search_count_max` times.

        Returns:
            FlatSolutionDict: The (updated) solution.
        """  # noqa: E501
        for _ in range(search_count_max):
            s_d = FlatSolutionDict(combined_solution.copy())
            optz = self._optimizers[self._rng.choice(len(self._optimizers))]
            optz_vars = optz.objective.variables
            x = s_d.to_solution(optz_vars).to_structured()
            x = optz_vars.generate_random_value(self._rng, x)
            s_d.update(x.to_flat().to_solution_dict())
            if self._is_satisfied(s_d):
                return s_d
        return combined_solution

    def _combine_solutions(self, individual_solutions: list[StructuredSolution]) -> FlatSolutionDict:
        """Combine a list of solution value vectors for individual objectives to a combined solution dict.

        Args:
            individual_solutions (list[StructuredSolution]): A list of solution value vectors for individual objectives.

        Returns:
            FlatSolutionDict: A combined solution including decision variables valules for the all objectives.
        """
        ret = FlatSolutionDict()
        for i in range(len(self._optimizers)):
            sol = individual_solutions[i]
            ret.update(sol.to_flat().to_solution_dict())
        return ret

    def _divide_into_solutions(self, combined_solution: FlatSolutionDict) -> list[StructuredSolution]:
        """Divide a combined solution (i.e. return from :obj:`MultiObjectiveOptimizer._combine_solutions`) to a list of solution vectors for individual objectives.

        Args:
            combined_solution (FlatSolutionDict): A combined solution.

        Returns:
            list[StructuredSolution]: A list of solution vectors for individual objectives.
        """  # noqa: E501
        ret: list[StructuredSolution] = []
        for optz in self._optimizers:
            sol = combined_solution.to_solution(optz.objective.variables).to_structured()
            ret.append(sol)
        return ret

    def _ensure_uniqueness(
        self, individual_solutions: list[StructuredSolution], search_count_max: int
    ) -> tuple[list[StructuredSolution], bool]:
        """Ensure the uniqueness of the found solution.

        If the solution is not unique, return a randomly generated alternative solution that is close to the original solution. This new solution should satisfy all the variable-related and user-defined constraints.

        Args:
            individual_solutions (list[StructuredSolution]): A list of solution vectors for individual objectives.
            search_count_max (int): Alternative solution close to the original solution is searched for at most `search_count_max` times.

        Returns:
            tuple[list[StructuredSolution], bool]: The updated unique solution (a list of solution vectors for individual objectives) considering constraints, and whether the solution is modified.
        """  # noqa: E501
        original_individual_solutions = individual_solutions
        for i in range(search_count_max):
            combined_solution = self._combine_solutions(individual_solutions)
            if self.data.is_unique(combined_solution):
                return individual_solutions, i != 0

            logger().info(f"identical input was obtained ({i}), x_hat={combined_solution}.")
            combined_solution = self._generate_alternative_solution(combined_solution, search_count_max)
            individual_solutions = self._divide_into_solutions(combined_solution)
        logger().warning("No alternative solution was found. Returning the original solution.")
        return original_individual_solutions, False

    def _anneal(
        self, model: amplify.Model, num_solves: int = 1, show_annealing_history: bool = False
    ) -> list[StructuredSolution]:
        """Perform annealing for the constructed `amplify.Model` with constraints.

        Args:
            model (amplify.Model): An Amplify-SDK model (`amplify.Model`).
            num_solves (int, optional): A number of serial solver execution in the Amplify SDK's serial solver execution (https://amplify.fixstars.com/en/docs/amplify/v1/serial.html). Defaults to 1.
            show_annealing_history (bool, optional): True to show a annealing history with time stamp. Available when Amplify Annealing Engine (`amplify.FixstarsClient`) is specified as the client in the constructor. Defaults to False.

        Raises:
            RuntimeError: If no solution is found.

        Returns:
            list[StructuredSolution]: The found solution (a list of solution vectors for individual objectives).
        """  # noqa: E501
        result = amplify.solve(model, self._client, num_solves=num_solves)
        if len(result.solutions) > 0:
            if show_annealing_history:
                anneal_history(result)
            ret: list[StructuredSolution] = []
            for optz in self._optimizers:
                optz_vars = optz.objective.variables
                q = optz_vars.poly_array
                ret.append(optz_vars.decode(q.evaluate(result.best.values).tolist()))
            return ret
        raise RuntimeError("No solution was found.")

    @property
    def i_cycle(self) -> int:
        """The number of current optimization cycle."""
        return self._i_cycle

    @property
    def data(self) -> DataList:
        """The current training data."""
        return self._data

    @property
    def amplify_model(self) -> amplify.Model | None:
        """The current Amplify-SDK model. If the model is not constructed yet, return `None`."""
        return self._amplify_model

    def fetch_history(self) -> History:
        """Return the optimization history. In multiple-objective optimization, number of initial traininig samples contained in the history is always zero (as individual datasets do not always meet constraints and duplicate variables across objectives).

        Returns:
            History: The optimization history.
        """  # noqa: E501
        # index = ["Sample #" + str(i) for i in range(len(self._data))]
        custom_objs: list[float] = []
        for i in range(len(self._data)):
            solution = self._divide_into_solutions(self._data.to_solution_dict(i))
            # custom objective (self._evaluate_custom_objective returns 0 if no custom obj is set)
            custom_objs.append(self._evaluate_custom_objective(solution))

        return History(self._data, self._elapsed_time, self._is_de_duplication, custom_objs)
