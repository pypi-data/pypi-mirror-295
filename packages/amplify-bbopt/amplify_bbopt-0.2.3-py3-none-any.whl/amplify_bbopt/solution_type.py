# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Any, Union

if TYPE_CHECKING:
    from collections.abc import Iterator

    from .variables import Variables

from .variable import VariableListBase


class FlatSolutionDict(dict[str, Union[bool, int, float]]):
    """Solution dictionary type with a :obj:`FlatSolution` compatible structure."""

    def __setitem__(self, key: str, value: bool | int | float) -> None:  # noqa: PYI041
        """Set item.

        Args:
            key (str): Key.
            value (bool | int | float): Value.

        Raises:
            TypeError: If a solution element has a :obj:`StructuredSolution` element form.
        """
        if isinstance(value, list):
            raise TypeError(
                "value must be a flat solution value, i.e. a variable list value must be expanded."
                " Use StructuredSolutionDict instead."
            )
        super().__setitem__(key, value)

    def to_solution(self, variables: Variables) -> FlatSolution:
        """Convert this solution dictionary to a :obj:`FlatSolution` class instance.

        Args:
            variables (Variables): Variables relevant to this solution.

        Returns:
            FlatSolution: The converted solution.
        """
        return FlatSolution(variables).from_solution_dict(self)

    def to_list(self) -> list[bool | int | float]:
        """Convert to a :obj:`FlatSolution`-compatible list (drop the names of variables).

        Returns:
            list[bool | int | float]: The solution.
        """
        return list(self.values())


class StructuredSolutionDict(dict[str, Union[bool, int, float, list[bool], list[int], list[float]]]):
    """Solution dictionary type with a :obj:`StructuredSolution` compatible structure."""

    def __setitem__(self, key: str, value: bool | int | float | list[bool] | list[int] | list[float]) -> None:  # noqa: PYI041
        """Set item.

        Args:
            key (str): Key.
            value (bool | int | float | list[bool] | list[int] | list[float]): Value.
        """
        super().__setitem__(key, value)

    def to_solution(self, variables: Variables) -> StructuredSolution:
        """Convert this solution dictionary to a :obj:`StructuredSolution` class instance.

        Args:
            variables (Variables): Variables relevant to this solution.

        Returns:
            FlatSolution: The converted solution.
        """
        return StructuredSolution(variables).from_solution_dict(self)

    def to_list(self) -> list[bool | int | float | list[bool] | list[int] | list[float]]:
        """Convert to a :obj:`StructuredSolution`-compatible list (drop the names of variables).

        Returns:
            list[bool | int | float | list[bool] | list[int] | list[float]]: The solution.
        """
        return list(self.values())


class FlatSolution:
    """Class for a solution vector type in a 'flat' form.

    An example flat form is [1, 2, 3, 4, 5], when (for example) 1 and 2 are the result from two elemental variables (e.g. :obj:`IntegerVariable`), and [2, 3, 4] is a result of a 'variable list' (:obj:`IntegerVariableList`) which contains three elemental variables. There is no structual indication of the 'variable list' values, and all elemental variables are flattened out.
    """  # noqa: E501

    def __init__(self, variables: Variables, x: list[bool | int | float] | None = None) -> None:
        """Initialize the class.

        Args:
            variables (Variables): Decision variables directly related to the solution.
            x (list[bool  |  int  |  float] | None, optional): A solution value vector. Defaults to `None`.
        """
        self._values: list[bool | int | float] = [] if x is None else x
        self._variables = variables
        self._names = self._get_names()

    @property
    def values(self) -> list[bool | int | float]:
        """The solution vector in a 'flat' form."""
        return self._values

    def to_structured(self) -> StructuredSolution:
        """Convert to :obj:`StructuredSolution`.

        Raises:
            ValueError: If length of the input value vector is not same as :obj:`Variables.num_elemental_variables`.

        Returns:
            StructuredSolution: The solution value vector.
        """
        if self._variables.num_elemental_variables != len(self._values):
            raise ValueError(
                "variables.num_elemental_variables must be equal to len(values) "
                f"{self._variables.num_elemental_variables} != {len(self._values)}."
            )
        x = StructuredSolution(self._variables)
        start = 0
        for v in self._variables.var_dict.values():
            if isinstance(v, VariableListBase):
                x.values.append(self._values[start : start + v.len])
            else:
                x.values.append(self._values[start])
            start += v.len
        return x

    def __len__(self) -> int:
        """The length of the solution vector.

        Note that in :obj:`FlatSolution`, a variable list element with the size N is counted as N in the length.

        Returns:
            int: length
        """
        return len(self._values)

    def __getitem__(self, i: int) -> tuple[str, bool | int | float]:
        """Return a tuple of a variable name and a corresponding value in the solution.

        Args:
            i (int): Index.

        Returns:
            tuple[str, bool | int | float]: A tuple of the variable name and a corresponding value.
        """
        return self._names[i], self._values[i]

    def __iter__(self) -> Iterator[tuple]:
        """A tuple of a variable name and a corresponding value.

        Yields:
            tuple[str, bool | int | float]: A tuple of a variable name and a corresponding value
        """
        yield from zip(self._names, self._values)

    @property
    def names(self) -> list[str]:
        """A list of names of variables in the solution.

        Note that in :obj:`FlatSolution`, a name of variable list is NOT considered. Rather, names of its elemental variables are considered in the list of names.
        """  # noqa: E501
        return self._names

    def _get_names(self) -> list[str]:
        """Get names of the variables.

        Returns:
            list[str]: The names of the variables.
        """
        names: list[str] = []
        for var in self._variables.var_dict.values():
            if isinstance(var, VariableListBase):
                var_names: list[str] = [v.name for v in var if v.name is not None]
                names += var_names
            else:
                assert var.name is not None
                names.append(var.name)
        return names

    def to_solution_dict(self) -> FlatSolutionDict:
        """Return the corresponding :obj:`FlatSolutionDict` class instance.

        Returns:
            FlatSolutionDict: The convrted solution.
        """
        ret = FlatSolutionDict()
        for k, v in self:
            ret[k] = v
        return ret

    def from_solution_dict(self, solution_dict_universe: dict[str, Any] | FlatSolutionDict) -> FlatSolution:
        """Construct :obj:`FlatSolution` solution from a solution dictionary or :obj:`FlatSolution`.

        Args:
            solution_dict_universe (dict[str, Any] | FlatSolutionDict): A solution dictionary. This can contains values for variables other than the ones exist in the solution. I.e. `solution_dict_universe` can be a entire solution for a multi-objective optimization whereas this class discribes an individual solution of one of the objective functions.

        Returns:
            FlatSolution: The solution.
        """  # noqa: E501
        solution: list[Any] = []
        for key, var in self._variables.var_dict.items():
            if isinstance(var, VariableListBase):
                var_solution = [solution_dict_universe[v.name] for v in var if v.name is not None]
                solution += var_solution
            else:
                solution.append(solution_dict_universe[key])
        self._values = solution
        return self

    def copy(self) -> FlatSolution:
        """Duplicate the class instance.

        Returns:
            FlatSolution: The duplicated class instance.
        """
        return FlatSolution(self._variables, copy.deepcopy(self._values))


class StructuredSolution:
    """Class for an solution vector in a 'structured' form.

    A Structured form is [1, [2, 3, 4], 5], when 1 and 5 are the result of two elemental variable (say, :obj:`IntegerVariable`) and [2, 3, 4] is a result of a 'variable list' (e.g. :obj:`IntegerVariableList`) containing three elemental variables. The structured form can show the structual indication of the variable list in the solution vector.
    """  # noqa: E501

    def __init__(
        self,
        variables: Variables,
        x: list[bool | int | float | list[bool] | list[int] | list[float]] | None = None,
    ) -> None:
        """Initialize the class.

        Args:
            variables (Variables): Decision variables directly related to the solution.
            x (list[bool  |  int  |  float  |  list[bool]  |  list[int]  |  list[float]] | None, optional): A solution value vector. Defaults to `None`.
        """  # noqa: E501
        self._values: list[bool | int | float | list[bool] | list[int] | list[float]] = x if x is not None else []
        self._variables = variables
        self._names = self._variables.names

    @property
    def values(self) -> list[bool | int | float | list[bool] | list[int] | list[float]]:
        """The solution vector in a 'structured' list."""
        return self._values

    def to_flat(self) -> FlatSolution:
        """Convert to the :obj:`FlatSolution`.

        Raises:
            ValueError: If the number of variables does not match to the number of the element in the value list.

        Returns:
            FlatSolution: The converted solution.
        """
        if len(self._variables) != len(self._values):
            raise ValueError(
                f"The number of variables {len(self._variables)} "
                f"must be equal to the elements in the list {len(self._values)}."
            )

        x = FlatSolution(self._variables)
        for item in self.values:
            if isinstance(item, list):
                x._values += item  # noqa: SLF001
            else:
                x._values.append(item)  # noqa: SLF001
        return x

    def __len__(self) -> int:
        """The length of the solution.

        Note that in :obj:`StructuredSolution`, a variable list element is counted as 1 in the length.

        Returns:
            int: The length.
        """
        return len(self._values)

    def __getitem__(self, i: int) -> tuple[str, bool | int | float | list[bool] | list[int] | list[float]]:
        """Return a tuple of a variable name and a corresponding value.

        Args:
            i (int): Index.

        Returns:
            tuple[str, bool | int | float | list[bool] | list[int] | list[float]]: A tuple of a variable name and a corresponding value.
        """  # noqa: E501
        return self._names[i], self._values[i]

    def __iter__(self) -> Iterator[tuple]:
        yield from zip(self._names, self._values)

    @property
    def names(self) -> list[str]:
        """The names of the variables.

        Note that in :obj:`StructuredSolution`, a name of variable list is considered, rather than the its elemental variables' names.
        """  # noqa: E501
        return self._names

    def to_solution_dict(self) -> StructuredSolutionDict:
        """Return corresponding :obj:`StructuredSolutionDict` class instance.

        Returns:
            StructuredSolutionDict: The solution dictionary of a variable (list) name and value(s) with a 'structure'd format..
        """  # noqa: E501
        ret = StructuredSolutionDict()
        for k, v in self:
            ret[k] = v
        return ret

    def from_solution_dict(self, solution_dict_universe: dict[str, Any] | StructuredSolutionDict) -> StructuredSolution:
        """Construct a solution in :obj:`StructuredSolution` from a solution dictionary with a 'structured' format.

        Args:
            solution_dict_universe (dict[str, Any] | StructuredSolutionDict): A solution dictionary with a 'structured' format. This can contains values for variables other than the ones exist in the solution. I.e. `solution_dict_universe` can be a entire solution for a multi-objective optimization whereas this class discribes an individual solution of one of the objective functions.

        Returns:
            StructuredSolution: The converted solution.
        """  # noqa: E501
        solution: list[Any] = [solution_dict_universe[key] for key in self._variables.var_dict]
        self._values = solution
        return self

    def copy(self) -> StructuredSolution:
        """Duplicate the class instance.

        Returns:
            StructuredSolution: The duplicated class instance.
        """
        return StructuredSolution(self._variables, copy.deepcopy(self._values))
