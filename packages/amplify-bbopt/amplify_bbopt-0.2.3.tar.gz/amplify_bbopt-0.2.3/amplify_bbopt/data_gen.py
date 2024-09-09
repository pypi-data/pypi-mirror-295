# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from typing import Any

import numpy as np

from .bb_func import BlackBoxFuncBase, BlackBoxFuncList
from .data_list import DataList
from .logger import logger
from .misc import exec_func_neat_stdout, header_obj, long_line
from .solution_type import FlatSolutionDict, StructuredSolution

RANDOM = "random"


class DatasetGenerator:
    """A generator of (random) input-output pairs of black-box function(s) as initial data for black-box optimization."""  # noqa: E501

    def __init__(
        self,
        objective: BlackBoxFuncBase | list[BlackBoxFuncBase],
        meet_constraints: bool = True,
        seed: int = 0,
    ) -> None:
        """Initialize the generator.

        For multiple-objective optimization, you can:

        (1) Specify multiple black-box function class instances in a list. By doing so, the generated dataset for each black-box objective function satisfies all the user-defined constraints for variables across all black-box opbjective functions as well.

        (2) Create and execute :obj:`DatasetGenerator.generate` for each of black-box objective function classes independently. You can set different number of samples in the dataset for different objective function class instances. This method is useful when you have training datasets for some of the objective functions, and only need to generate datasets for the rest of the objective functions. The drawback of this method is that if there are constraints that considers variables appearing different objective functions, the following `meet_constraints` has to be `False`, meaning such constraints are not considered in the initial dataset. If all constraints are about variables only used within the same objective function, such constraints can be considered here.

        Args:
            objective (BlackBoxFuncBase): A black-box function class instance for single objective optimization, or a list of multiple objective function class instances for multi-objectives.
            meet_constraints (bool, optional): True if generated input vectors must meet the constraints. Defaults to `True`.
            seed (int, optional): A random seed. Defaults to 0.
        """  # noqa: E501
        if isinstance(objective, list):
            self._objectives = BlackBoxFuncList(objective)
        else:
            self._objectives = BlackBoxFuncList([objective])
        self._meet_constraints = meet_constraints

        if len(self._objectives.constraints) == 0:
            self._meet_constraints = False

        self._rng = np.random.default_rng(seed)

    def _gen_input(self, method: str = RANDOM) -> FlatSolutionDict:
        """Generate an input value vector by using the method specified.

        Args:
            method (str, optional): A generation method. Defaults to `"random"`.

        Raises:
            ValueError: If the specified method is invalid.

        Returns:
            FlatSolutionDict: The generated input vector.
        """
        if method == RANDOM:
            solution_list: list[StructuredSolution] = [
                obj.variables.generate_random_value(self._rng) for obj in self._objectives
            ]
            solution_dict = FlatSolutionDict()
            for solution in solution_list:
                solution_dict.update(solution.to_flat().to_solution_dict())

            return solution_dict
        raise ValueError(f"Invalid method is specified: {method}.")

    def _generate_input_constrained(
        self,
        method: str = RANDOM,
    ) -> FlatSolutionDict:
        """Generate an input vector that satisfies the user-defined constraints.

        Args:
            method (str, optional): A generation method. Defaults to `"random"`.

        Returns:
            FlatSolutionDict: The generated input vector.
        """
        is_satisfied = False
        while not is_satisfied:
            solution_dict = self._gen_input(method)
            if not self._meet_constraints:
                break
            is_satisfied = self._objectives.constraints.is_satisfied(solution_dict)

        return solution_dict

    def _generate_inputs(self, num_inputs: int, method: str = RANDOM) -> DataList:
        """Generate multiple unique inputs. These inputs also satisfy all user-defined constraints if `meet_constraints = True` in :obj:`DatasetGenerator.__init__`.

        Args:
            num_inputs (int): A number of inputs to generate.
            method (str, optional): A generation method. Defaults to `"random"`.

        Returns:
            DataList: A list of the generated input vectors.
        """  # noqa: E501
        data_list = DataList(variable_names=self._objectives.variable_names)

        solution_dict = self._generate_input_constrained(method)
        data_list.append((list(solution_dict.values()), 0))

        for _ in range(num_inputs - 1):
            while not data_list.is_unique(solution_dict):
                solution_dict = self._generate_input_constrained(method)
            data_list.append((list(solution_dict.values()), 0))
        return data_list

    def generate(self, num_samples: int, method: str = RANDOM) -> Any:  # noqa: ANN401
        """Generate a dataset consisting multiple unique input-output pairs. These inputs also satisfy all user-defined constraints if `meet_constraints = True` in :obj:`DatasetGenerator.__init__`.

        Args:
            num_samples (int): A number of input-output pairs to generate.
            method (str, optional): A generation method. Defaults to `"random"`.

        Returns:
            DataList | tuple[DataList, ...]: The generated dataset with multiple input-output pairs. If multiple objective functions in a list are passed in :obj:`DatasetGenerator.__init__`, return multiple datasets in a tuple, each corresponds to one of the objective functions in a  respective order.
        """  # noqa: E501
        data_list_all_df = self._generate_inputs(num_samples, method).to_df()

        data_list_list: list[DataList] = []

        # Evaluate each objective function
        for obj in self._objectives:
            data_list = DataList(variable_names=obj.variables.flat_names)
            for i in range(num_samples):
                logger().info(long_line)
                logger().info(f"#{i}/{num_samples} initial data for {obj.name}")

                solution_dict_all = FlatSolutionDict(data_list_all_df.iloc[i].to_dict())
                # extract values only relevant to individual objective function
                solution = solution_dict_all.to_solution(obj.variables).to_structured()
                solution_dict = solution.to_solution_dict()
                y_evaluated = exec_func_neat_stdout(header_obj, obj._call_objective, logger(), **solution_dict)  # type: ignore # noqa: SLF001

                data_list.append((list(solution.to_flat().values), y_evaluated))

            data_list_list.append(data_list)

        if len(self._objectives) == 1:
            return data_list_list[0]

        return tuple(data_list_list)
        return tuple(data_list_list)
