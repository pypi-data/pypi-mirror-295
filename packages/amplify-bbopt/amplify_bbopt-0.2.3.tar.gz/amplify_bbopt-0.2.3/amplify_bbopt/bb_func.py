# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

import abc
import contextlib
import inspect
import time
from typing import TYPE_CHECKING, Any, Callable, get_type_hints

from .constraint import Constraint, Constraints
from .variable import VariableBase, VariableListBase
from .variables import Variables

if TYPE_CHECKING:
    from collections.abc import Generator, Iterator


class BlackBoxFuncBase(abc.ABC):
    """Base class to define a black box objective function class.

    Args:
        abc: Abstract base class.
    """

    def __init__(self) -> None:
        """Initialize the base class."""
        self._variables = Variables()
        self._constraints = Constraints()
        self._name = f"bb_func_{time.perf_counter_ns()}"

    @property
    def name(self) -> str:
        """Name of the black-box objective function."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set a black-box function name. If a black-box function class is defined by using the :obj:`blackbox` decorator, the name is automatically set.

        Args:
            value (str): A black-box function name.
        """  # noqa: E501
        self._name = value

    def __setattr__(self, name: str, value: Any) -> None:  # noqa: ANN401
        """Set decision variables.

        Args:
            name (str): The name of a decision variable.
            value (Any): A decision variable.
        """
        super().__setattr__(name, value)
        if isinstance(value, (VariableBase, VariableListBase)):
            self._variables._set_variable(name, value)  # noqa: SLF001
        elif name in self._variables.var_dict:
            self._variables._del_variable(name)  # noqa: SLF001

    def _call_objective(self, **kwargs: bool | int | float | list[bool] | list[int] | list[float]) -> float:  # noqa: PYI041
        """Call the objective function with input arguments to the function.

        Returns:
            float: The objective function value.
        """

        @contextlib.contextmanager
        def replace_ctx() -> Generator[Any, Any, Any]:
            try:
                # Replace variables with values
                for pred_name, pred_value in kwargs.items():
                    if pred_name in self._variables.var_dict:
                        super(BlackBoxFuncBase, self).__setattr__(pred_name, pred_value)
                yield
            finally:
                # Replace values with variables
                for name, bb_var in self._variables.var_dict.items():
                    self.__setattr__(name, bb_var)  # noqa: PLC2801

        with replace_ctx():
            return self.objective()

    @property
    def variables(self) -> Variables:
        """Decision variables associated with this black-box objective function."""
        return self._variables

    @abc.abstractmethod
    def objective(self) -> float:
        """Evaluate the objective function. An evaluator sets the class variable attributes having the names and valueas of the input.

        Returns:
            float: An objective function value.
        """  # noqa: E501

    def add_constraint(
        self,
        constraint: Constraint | Constraints | list[Constraint | Constraints] | list[Constraint] | list[Constraints],
    ) -> None:
        """Add user-defined constraints to the black-box function class instance.

        Args:
            constraint (Constraint | Constraints | list[Constraint | Constraints] | list[Constraint] | list[Constraints]): User-defined constraints.
        """  # noqa: E501
        self._constraints.append(constraint)

    @property
    def constraints(self) -> Constraints:
        """User-defined constraints associated with this black-box function class."""
        return self._constraints


def blackbox(func: Callable) -> BlackBoxFuncBase:
    """Decorator function to create a black-box objective function class instance.

    Args:
        func (Callable): A black-box objective function.

    Raises:
        ValueError: If decision variables are not appropriately set for the input arguments to a black-box function.

    Returns:
        BlackBoxFunc: A black-box function class instance which associates a black-box function and decision variables.
    """
    parameters = inspect.signature(func).parameters
    arguments = {v.name for v in parameters.values()}

    # Set variables defined as default values
    variables = Variables()
    for k, v in parameters.items():
        if isinstance(v.default, (VariableBase, VariableListBase)):
            variables._set_variable(k, v.default)  # noqa: SLF001

    # Set variables defined with Annotated
    annotations = get_type_hints(func, include_extras=True)
    for k, v in annotations.items():
        if k == "return":
            continue
        if (
            hasattr(v, "__metadata__")
            and len(v.__metadata__) == 1
            and isinstance(v.__metadata__[0], (VariableBase, VariableListBase))
        ):
            variables._set_variable(k, v.__metadata__[0])  # noqa: SLF001

    missing_args = arguments - set(variables.names)
    if len(missing_args) != 0:
        for arg in missing_args:
            raise ValueError(
                f"Argument `{arg}` of {func.__name__} must be annotated with `Annotated[..., Variable(...)`"
                f" or has a default value as `Variable`."
            )

    class BlackBoxFunc(BlackBoxFuncBase):
        def __init__(self) -> None:  # type: ignore
            super().__init__()
            self._name = func.__name__
            for name, variable in variables.var_dict.items():
                setattr(self, name, variable)

        def __call__(self, *args, **kwargs) -> float:  # noqa: ANN002, ANN003
            return func(*args, **kwargs)

        def objective(self) -> float:
            return func(**{k: getattr(self, k) for k in self._variables.var_dict})

    return BlackBoxFunc()


class BlackBoxFuncList:
    """Class handles multiple black-box objective functions for multi-objective optimization."""

    def __init__(self, objectives: list[BlackBoxFuncBase], unify_variables: bool = False) -> None:
        """Initialize a black-box function list class.

        Args:
            objectives (list[BlackBoxFuncBase]): A list of class instances of black-box functions to be considered in multi-objective optimization.
            unify_variables (bool, optional): Whether to unify variables and constraints of multiple objectives in :obj:`BlackBoxFuncList.handle_duplicates`). Note that if you are performing multi-objective optimizations and want to manually operate `amplify.PolyArray` for variables (e.g. for creating custom constraints), this has to be done AFTER the last execution of :obj:`BlackBoxFuncList.handle_duplicates` with `unify_variables = True`. Since this unification is expected to be executed in the initializers of the optimizers, such operation usually should be done after the instantiation of the relevant optimizers. Defaults to `False`.
        """  # noqa: E501
        self._objectives: list[BlackBoxFuncBase] = []

        self._constraints = Constraints()
        for bb_func in objectives:
            self._objectives.append(bb_func)
            self._constraints.append(bb_func.constraints)
        self._unify_variables = unify_variables
        self.handle_duplicates()

    def handle_duplicates(self) -> None:
        """Handle redundancy of variables and consistent issuance of `amplify.PolyArray` for different black-box objective functions, and unify variables and constraints. Expected to call this each time there is change in the objective functions to consider. The unification happens when `unify_variables = True` in :obj:`BlackBoxFuncList.__init__`."""  # noqa: E501
        # Variable dictionary
        var_dict_universe: dict[str, Any] = {}
        for bb_func in self._objectives:
            var_dict_universe.update(bb_func.variables.var_dict)

        elemental_variable_name_list: list[str] = []
        for bb_func in self._objectives:
            elemental_variable_name_list += bb_func.variables.flat_names
        self._variable_names = list(dict.fromkeys(elemental_variable_name_list))

        if self._unify_variables:
            # Nullify all existing Amplify SDK's variables.
            for i, bb_func in enumerate(self._objectives):
                bb_func.variables.nullify_poly_array(i)
            # Update Variables.var_dict and re-issue Amplify SDK variables.
            variable_generator_common = self._objectives[0].variables.variable_generator
            for bb_func in self._objectives:
                bb_func.variables.unify_variables(var_dict_universe, variable_generator_common)
            # Reconstruct constraints based on unified variables described in Variables.var_dict.
            for bb_func in self._objectives:
                bb_func.constraints.unify_variables(var_dict_universe)

    def __getattr__(self, name: str) -> BlackBoxFuncBase:
        """Get a variable in var_dict.

        Raises:
            ValueError: If the specified object is not found.

        Returns:
            BlackBoxFuncBase: A black-box function class instance.
        """
        names = [obj.name for obj in self._objectives]

        if name not in names:
            raise ValueError(f"No such objective {name} is found. [{names}].")
        return self._objectives[names.index(name)]

    def add_constraint(
        self,
        constraint: Constraint | Constraints | list[Constraint | Constraints] | list[Constraint] | list[Constraints],
    ) -> None:
        """Add a user-defined constraint to the black-box function class.

        Args:
            constraint ( constraint: Constraint | Constraints | list[Constraint | Constraints] | list[Constraint] | list[Constraints]): User-defined constraints.
        """  # noqa: E501
        self._constraints.append(constraint)

    def append(self, bb: BlackBoxFuncBase) -> None:
        """Append a black-box function class.

        Args:
            bb (BlackBoxFuncBase): A black-box function class instance.
        """
        self._objectives.append(bb)
        self.handle_duplicates()

    def __len__(self) -> int:
        """Return a number of black-box function class instances."""
        return len(self._objectives)

    def __getitem__(self, i: int) -> BlackBoxFuncBase:
        """Return the i-th black-box function class instance.

        Args:
            i (int): Index of a black-box function class instance.

        Returns:
            BlackBoxFuncBase: The i-th black-box function class instance.
        """
        return self._objectives[i]

    def __iter__(self) -> Iterator[BlackBoxFuncBase]:
        """The list of black-box function class instances.

        Yields:
            Iterator[BlackBoxFuncBase]: A black-box function class instance.
        """
        yield from self._objectives

    @property
    def constraints(self) -> Constraints:
        """Constraints associated with this black-box function list."""
        return self._constraints

    @property
    def variable_names(self) -> list[str]:
        """Names of variables associated with this black-box function list."""
        return self._variable_names
