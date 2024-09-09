# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

import copy
import math
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterator

import amplify
import numpy as np
import pandas as pd

from .logger import logger
from .misc import print_to_str
from .poly import Poly

# Encoding method
DOMAIN_WALL = "domain_wall"  # default
ONEHOT = "one_hot"
# Amplify SDK handles variable encoding with "default" (FM considers non-binary variables)
AMPLIFY = "amplify"


def field(var: Any) -> Any:  # noqa: ANN401
    """Wrapper for Variable but annotated with Any type."""
    return var  # noqa: DOC201


@field
class Variable(ABC):
    """A base class for all variables."""

    def __init__(
        self,
        var_type: type,
        bounds: tuple,
        delta: float,
        nbins: int,
        method: str | None = DOMAIN_WALL,
    ) -> None:
        """Constructor for a decision variable.

        Args:
            var_type (type): A type of the variable.
            bounds (tuple): A lower and upper bounds that the variable can take.
            delta (float): A discretization step width.
            nbins (int): A number of dicsretization bins.
            method (str | None, optional): Encoding method. 'dw': domain-wall. 'one_hot': one-hot. 'amplify': Amplify SDK's encoder. Defaults to 'dw'.

        Raises:
            ValueError: If the lower bound is greater than the upper bound.
            ValueError: If the given encoding method is invalid.
        """  # noqa: E501
        if bounds[0] >= bounds[1]:
            raise ValueError(f"The lower bound must be less than the upper bound. {bounds=}.")
        self._type = var_type
        self._bounds = bounds
        self._nbins = nbins
        self._delta = delta
        if method in {DOMAIN_WALL, ONEHOT, AMPLIFY} or method is None:
            pass  # do nothing
        else:
            raise ValueError(f"{method=} is invalid")

        self._method = method
        self._name: str | None = None
        self._len = 1

        self._poly_array: amplify.PolyArray | None = None

    @property
    def discrete_domain(self) -> list | None:
        if isinstance(self, (IntegerVariable, IntegerVariableList)):
            return list(range(self.bounds[0], self.bounds[1] + 1))
        if isinstance(self, (BinaryVariable, BinaryVariableList)):
            return [False, True]
        if isinstance(self, DiscreteVariable):
            return self._discretized_list  # type: ignore
        if isinstance(self, DiscreteVariableList):
            return self[0].discretized_list  # type: ignore
        return None

    def to_poly(self) -> Poly:
        """Convert the variable to a polynomial with a unity coefficient.

        If this is directly called for
        a variable list class instance, the sum of all the variables in the list is considered.

        Returns:
            Poly: The constructed polynomial.
        """
        return Poly({self: 1.0})

    def __mul__(self, other: Any) -> Poly:  # noqa: ANN401
        """Multiply the variable by a value.

        If this is directly called for a variable list class,
        the sum of all the variables applied `__mul__` is considered.

        Args:
            other: A value to multiply.

        Returns:
            Poly: The resulting polynomial of the variable with a coefficient being the value.
        """
        return Poly({self: other})

    def __rmul__(self, other: Any) -> Poly:  # noqa: ANN401
        """Multiply the variable by a value.

        If this is directly called for a variable list class,
        the sum of all the variables applied `__rmul__` is considered.

        Args:
            other: A value to multiply.

        Returns:
            Poly: The resulting polynomial of the variable with a coefficient being the value.
        """
        return Poly({self: other})

    def __add__(self, other: Any) -> Poly:  # noqa: ANN401
        """Add the variable to another variable or a polynomial.

        Args:
            other: A variable or a polynomial to add.

        Raises:
            ValueError: If other is not a variable or a polynomial.

        Returns:
            Poly: The resulting polynomial.
        """
        if isinstance(other, (VariableBase, VariableListBase)):
            return self.to_poly() + other.to_poly()
        if isinstance(other, Poly):
            return self.to_poly() + other
        raise ValueError(f"{other} has type {type(other)}.")

    def __sub__(self, other: Any) -> Poly:  # noqa: ANN401
        """Subtract another variable or a polynomial from the variable.

        Args:
            other: A variable or a polynomial to subtract.

        Raises:
            ValueError: If other is not a variable or a polynomial.

        Returns:
            Poly: The resulting polynomial.
        """
        if isinstance(other, VariableBase):
            return self.to_poly() - other.to_poly()
        if isinstance(other, Poly):
            return self.to_poly() - other
        raise ValueError(f"{other} has type {type(other)}.")

    def __radd__(self, other: Any) -> Poly:  # noqa: ANN401
        """Add the variable to another variable or a polynomial.

        Args:
            other: A variable or a polynomial to add.

        Raises:
            ValueError: If other is not a variable or a polynomial.

        Returns:
            Poly: The resulting polynomial.
        """
        if isinstance(other, VariableBase):
            return self.to_poly() + other.to_poly()
        if isinstance(other, Poly):
            return self.to_poly() + other
        raise ValueError(f"{other} has type {type(other)}.")

    def __rsub__(self, other: Any) -> Poly:  # noqa: ANN401
        """Subtract another variable or a polynomial from the variable.

        Args:
            other: A variable or a polynomial to subtract.

        Raises:
            ValueError: If other is not a variable or a polynomial.

        Returns:
            Poly: The resulting polynomial.
        """
        if isinstance(other, VariableBase):
            return other.to_poly() - self.to_poly()
        if isinstance(other, Poly):
            return other - self.to_poly()
        raise ValueError(f"{other} has type {type(other)}.")

    @property
    def len(self) -> int:
        """Return the number of the variables. This is significant for variable list classes.

        Returns:
            int: The number of the variables.
        """
        return self._len

    @property
    def name(self) -> str | None:
        """Return the name of the variable.

        Returns:
            str: The variable name.
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        """Set the name of the variable.

        Args:
            name (str): The variable name.
        """
        self._name = name

    @property
    def type(self) -> type:
        """Return the type of the variable.

        Returns:
            type: The variable type.
        """
        return self._type

    @property
    def bounds(self) -> tuple:
        """Return the lower and upper bounds that the variable can take.

        Returns:
            The lower and upper bounds that the variable can take.
        """
        return self._bounds

    @property
    def nbins(self) -> int:
        """Return the number of discretization bins.

        Returns:
            int: The number of discretization bins.
        """
        return self._nbins

    @property
    def delta(self) -> float:
        """Return the distance between discretization points.

        Returns:
            The distance between discretization points.
        """
        return self._delta

    @property
    def method(self) -> str | None:
        """Return the encoding method.

        Returns:
            str | None: The encoding method. `None` is no encoding is necessary.
        """
        return self._method

    @property
    @abstractmethod
    def num_amplify_variables(self) -> int:
        """Return the number of the Amplify SDK variables encoded from this variable.

        Returns:
            int: The number of the Amplify SDK variables.
        """

    @abstractmethod
    def to_amplify_poly(self) -> amplify.Poly:
        """Convert the variable to the Amplify SDK's polynomial.

        Returns:
            amplify.Poly: The resulting polynomial.
        """

    @abstractmethod
    def encode(self, value: Any) -> list[int | Any]:  # noqa: ANN401
        """Encode the value to values of the Amplify SDK variables (i.e. binary variables) if necessary.

        Args:
            value (Any): The value to encode.

        Returns:
            list[int | Any]: The encoded value in the Amplify SDK variables (i.e. binary variables).
        """

    @abstractmethod
    def decode(self, encoded_value_vector: list[int | Any]) -> Any:  # noqa: ANN401
        """Decode values of the the Amplify SDK variables (i.e. binary variables) to a value of this variable.

        Args:
            encoded_value_vector (list[int | Any]): A list of the Amplify SDK variable values to decode.

        Returns:
            Any: The decoded value.
        """

    @abstractmethod
    def generate_amplify_constraint(self) -> amplify.ConstraintList:
        """Generate Amplify SDK's constraints related to the conversion of non-binary variable.

        Returns:
            amplify.ConstraintList: The resulting constraints.
        """

    @abstractmethod
    def generate_random_value(
        self,
        rng: np.random.Generator,
        ref_value: Any | None = None,  # noqa: ANN401
        find_neighbour: bool = False,
    ) -> Any:  # noqa: ANN401
        """Generate a random value compatible with the variable.

        If ref_value specified, ensure that the return value
        value != ref_value. User-defined constraints (if there's any) are not considered in this value.

        Args:
            rng (np.random.Generator): NumPy's random generator.
            ref_value (Any | None): A reference value. Defaults to `None`.
            find_neighbour (bool, optional): True to generate a random value neighbour to the reference value. Defaults to `False`.

        Returns:
            Any: The resulting value of the variable.
        """  # noqa: E501


@field
class VariableBase(Variable):
    """A base class for all elemental variables."""

    def __init__(
        self,
        var_type: type,
        bounds: tuple,
        delta: float,
        nbins: int,
        method: str | None = DOMAIN_WALL,
    ) -> None:
        """Constructor.

        Args:
            var_type (type): A type of the variable.
            bounds (tuple): A lower and upper bounds that the variable can take.
            delta (float): A discretization step width.
            nbins (int): A number of dicsretization bins.
            method (str | None, optional): Encoding method. 'dw': domain-wall. 'one_hot': one-hot. 'amplify': Amplify SDK's encoder. Defaults to 'dw'.
        """  # noqa: E501
        super().__init__(var_type, bounds, delta, nbins, method)
        if method == DOMAIN_WALL:
            self._num_amplify_variables = nbins - 1
        elif method == AMPLIFY:
            self._num_amplify_variables = 1
        else:
            self._num_amplify_variables = nbins

    def nullify_poly_array(self) -> None:
        """Make poly_array = None."""
        self._poly_array = None

    @property
    def poly_array(self) -> amplify.PolyArray | None:
        """The Amplify SDK's `PolyArray` that represents this variable."""
        return self._poly_array

    @property
    def num_amplify_variables(self) -> int:
        """Return the number of the Amplify SDK variables encoded from the variable.

        Returns:
            int: The number of the Amplify SDK variables.
        """
        return self._num_amplify_variables

    def encode(self, value: Any) -> list[int | Any]:  # noqa: ANN401
        """Encode the value to values of the Amplify SDK variables (i.e. binary variables) if necessary.

        Args:
            value (Any): The value to encode.

        Returns:
            list[int | Any]: The encoded value in the form of the Amplify SDK variables (i.e. binary variables).
        """
        if self.method == AMPLIFY:
            return [value]

        return self.idx_to_binary(self.value_to_idx(value))

    def decode(self, amplify_value_vector: list[int | Any]) -> Any:  # noqa: ANN401
        """Decode values of the the Amplify SDK variables (i.e. binary variables) to a value of this variable.

        Args:
            amplify_value_vector (list[int | Any]): A list of the Amplify SDK variable values to decode.

        Returns:
            Any: The decoded value.
        """
        if self.method == AMPLIFY:
            return amplify_value_vector[0]
        return self.idx_to_value(self.binary_to_idx(np.array(amplify_value_vector).astype(int)))  # type: ignore

    @abstractmethod
    def value_to_idx(self, value: Any) -> int:  # noqa: ANN401
        """Convert a value of the variable to a value index.

        Args:
            value (Any): A value to convert.

        Returns:
            int: The value index.
        """

    @abstractmethod
    def idx_to_value(self, idx: int) -> Any:  # noqa: ANN401
        """Convert a value index to a value or a polynomial of the variable.

        Args:
            idx (int): A value index.

        Returns:
            Any: The value or a polynomial of the variable.
        """

    @abstractmethod
    def to_amplify_poly(self) -> amplify.Poly:
        """Convert the variable to the Amplify's `Poly` formulation. For a variable list class instance, the sum of all the variables in the list is considered.

        Returns:
            amplify.Poly: The resulting polynomial.
        """  # noqa: E501

    def issue_amplify_variable(
        self,
        generator: amplify.VariableGenerator,
        var_counter: dict[amplify.VariableType, int],
        var_name: dict[amplify.VariableType, str],
    ) -> None:
        """Issue the Amplify SDK's variables (`amplify.PolyArray`) for the variable only when `VariableBase.poly_array is None`.

        Args:
            generator (amplify.VariableGenerator): A variable generator.
            var_counter (dict[amplify.VariableType, int]): Counter counts how many amplify variables of each amplify.VariableType are issued.
            var_name (dict[amplify.VariableType, str]): Name prefix of amplify variables of each amplify.VariableType.
        """  # noqa: E501
        if self.poly_array is None:
            self.issue_amplify_variable_impl(generator, var_counter, var_name)

    @abstractmethod
    def issue_amplify_variable_impl(
        self,
        generator: amplify.VariableGenerator,
        var_counter: dict[amplify.VariableType, int],
        var_name: dict[amplify.VariableType, str],
    ) -> None:
        """Issue the Amplify SDK variables relevant to this variable."""

    def binary_to_idx(self, binary: list[int]) -> int:
        """Convert a binary vector to a value index of the variable.

        Args:
            binary (list[int]): The binary vector to convert.

        Raises:
            RuntimeError: If this method is called with the variable encoding method being `"amplify"`.

        Returns:
            int: The resulting value index.
        """
        if self.method == AMPLIFY:
            raise RuntimeError("This method should not be necessary when Amplify SDK does the encoding.")

        if self.method == ONEHOT:
            idx = (np.array(binary) * np.array(range(self.num_amplify_variables), dtype=int)).sum()
        else:  # domain wall
            idx = np.array(binary).sum()
        return idx

    def idx_to_binary(self, idx: int) -> list[int]:
        """Convert a value index to a binary vector.

        Args:
            idx (int): The value index to convert.

        Raises:
            RuntimeError: If this method is called with the variable encoding method being `"amplify"`.

        Returns:
            list[int]: The resulting binary vector.
        """
        if self.method == AMPLIFY:
            raise RuntimeError("This method should not be necessary when Amplify SDK does the encoding.")

        # TO-DO: limit the range of the given idx to (0, var_nbins)?
        x = np.zeros(self.num_amplify_variables, int)
        if self.method == ONEHOT:
            x[idx] = 1
        else:  # domain wall
            x[0:idx] = 1  # [1, 1, 0, 0, 0]...2
        return x.tolist()

    def generate_amplify_constraint(self) -> amplify.ConstraintList:
        """Generate Amplify SDK's constraints related to the conversion of a non-binary variable.

        Raises:
            RuntimeError: If the poly_array is not set.

        Returns:
            amplify.ConstraintList: The resulting constraints.
        """
        if self._poly_array is None:
            raise RuntimeError("poly array is not set.")

        if self.method is None or self.method == AMPLIFY:
            return amplify.ConstraintList()

        constraint = amplify.ConstraintList()
        if self.method == ONEHOT:
            constraint += amplify.one_hot(self._poly_array)
        else:  # domain wall
            constraint += amplify.domain_wall(self._poly_array, ascending=False)
        return constraint

    def generate_random_value(
        self,
        rng: np.random.Generator,
        ref_value: Any | None = None,  # noqa: ANN401
        find_neighbour: bool = False,
    ) -> Any:  # noqa: ANN401
        """Generate a random value compatible with the variable.

        If ref_value specified, ensure that the return value
        value != ref_value. User-defined constraints (if there's any) are not considered in this value.

        Args:
            rng (np.random.Generator): NumPy's random generator.
            ref_value (Any | None, optional): A reference value. Defaults to None.
            find_neighbour (bool, optional): True to generate a random value neighbour to the reference value. Defaults to `False`.

        Returns:
            Any: The resulting value of the variable.
        """  # noqa: E501
        if self.method == AMPLIFY:
            return self.type(rng.uniform(self.bounds[0], self.bounds[1]))

        idx_max = self.nbins + 1 if self.type is bool else self.nbins
        value = self.idx_to_value(rng.integers(idx_max))
        if ref_value is None:
            return value
        idx_min = 0
        if find_neighbour:
            idx = self.value_to_idx(ref_value)
            idx_min = max(0, idx - 1)
            idx_max = min(idx + 2, idx_max)

        max_search = 10
        for _ in range(max_search):
            value = self.idx_to_value(rng.integers(idx_min, idx_max))
            if value != ref_value:
                return value
        return ref_value  # this should not be happen generally (only when rng.integers == idx for max_search times...)

    def construct_discretize_table(self) -> np.ndarray:
        """Discretization information.

        Returns:
            np.ndarray: Discretization table.
        """
        if self.type is bool or self.method == AMPLIFY:
            return np.array([f"({self.bounds[0]}, {self.bounds[1]})"])
        return np.array([self.idx_to_value(i) for i in range(self.nbins)], self.type)

    def __str__(self) -> str:
        """Return a human-readable information of the variables.

        Returns:
            str: The human-readable information of the variables.
        """
        df = pd.DataFrame(index=[], columns=[f"i={i}" for i in range(self.nbins)])
        df.loc[self.name] = self.construct_discretize_table()
        ret = print_to_str(
            pd.concat(
                [
                    pd.DataFrame([self.type.__name__], index=df.index, columns=["type"]),
                    pd.DataFrame([self.nbins], index=df.index, columns=["nbins"]),
                    pd.DataFrame([self.len], index=df.index, columns=["len"]),
                    pd.DataFrame([self.method], index=df.index, columns=["method"]),
                    pd.DataFrame([self.num_amplify_variables], index=df.index, columns=["nvars"]),
                    df,
                ],
                axis=1,
            )
        )
        return ret.removesuffix("\n")


@field
class VariableListBase(Variable):
    """A base class for all variable lists."""

    def __init__(
        self,
        var_type: type,
        bounds: tuple,
        delta: float,
        nbins: int,
        length: int,
        method: str | None = DOMAIN_WALL,
    ) -> None:
        """Constructor.

        Args:
            var_type (type): A type of the variable.
            bounds (tuple): A lower and upper bounds that the variable can take.
            delta (float): A discretization step width.
            nbins (int): A number of dicsretization bins.
            length (int): A number of the variables in the list.
            method (str | None, optional): Encoding method. 'dw': domain-wall. 'one_hot': one-hot. 'amplify': Amplify SDK's encoder. Defaults to 'dw'.

        Raises:
            ValueError: If the length is equal to or less than 1.

        """  # noqa: E501
        if length < 2:  # noqa: PLR2004
            raise ValueError(f"The length of VariableList must be greater than 1. {length=}")
        super().__init__(var_type, bounds, delta, nbins, method)
        self._len = length
        self._variable_list: list[VariableBase] = []

    def nullify_poly_array(self) -> None:
        """Make poly_array = None for the elemental variables in the variable list."""
        for v in self.variable_list:
            v._poly_array = None  # noqa: SLF001
        self._poly_array = None

    @property
    def poly_array(self) -> amplify.PolyArray | None:
        """Return the Amplify SDK's `PolyArray` that represents all elemental variables existing in this variable list.

        Returns:
            amplify.PolyArray: The Amplify SDK's `PolyArray`.
        """
        ret: list[amplify.Poly] = []
        for v in self.variable_list:
            if v.poly_array is None:
                return None
            ret += v.poly_array.to_list()
        return amplify.PolyArray(ret)

    def __len__(self) -> int:
        """Return the number of the variables.

        Returns:
            int: The number of the variables.
        """
        return self.len

    def __getitem__(self, i: int) -> VariableBase:
        return self.variable_list[i]

    def __iter__(self) -> Iterator[VariableBase]:
        yield from self.variable_list

    def to_poly(self) -> Poly:
        """Return the polynomial that represents the sum of all the variables in the variable list class.

        Returns:
            Poly: The polynomial.
        """
        return np.array(self.variable_list).sum()

    def __mul__(self, other: Any) -> Poly:  # noqa: ANN401
        """Return the polynomial that represents the sum of all the variables multiplied by a value.

        Args:
            other: A value to multiply.

        Returns:
            Poly: The resulting polynomial.
        """
        return np.array([other * var for var in self]).sum()

    def __rmul__(self, other: Any) -> Poly:  # noqa: ANN401
        """Return the polynomial that represents the sum of all the variables multiplied by a value.

        Args:
            other: A value to multiply.

        Returns:
            Poly: The resulting polynomial.
        """
        return np.array([other * var for var in self]).sum()

    def sum(self) -> Poly:
        return self.to_poly()

    @property
    def num_amplify_variables(self) -> int:
        """Return the number of the Amplify SDK variables encoded from the variable.

        Returns:
            int: The number of the Amplify SDK variables.
        """
        return self.len * self.variable_list[0].num_amplify_variables

    @property
    def variable_list(self) -> list[VariableBase]:
        """Return the list of elemental variables in the variable list.

        Returns:
            list[VariableBase]: The list of the variables.
        """
        return self._variable_list

    def encode(self, value_list: list[Any]) -> list[int | Any]:
        """Encode the values to values of the Amplify SDK variables (i.e. binary variables) if necessary.

        Args:
            value_list (list[Any]): The values to encode.

        Returns:
            list[int | Any]: The encoded value in the form of the Amplify SDK variables (i.e. binary variables).
        """
        encoded: list[int | Any] = []
        for i, var in enumerate(self._variable_list):
            encoded += var.encode(value_list[i])
        return encoded

    def decode(self, amplify_value_vector: list[int | Any]) -> list[Any]:
        """Decodes values of the Amplify SDK variables (i.e. binary variables) to a list of values of this variable list.

        Args:
            amplify_value_vector (list[int | Any]): A list of the Amplify SDK variable values to decode.

        Returns:
            list[Any]: A list of the decoded values.
        """  # noqa: E501
        value_list: list[self.type] = []  # type: ignore
        for i, var in enumerate(self._variable_list):
            start = i * var.num_amplify_variables
            stop = start + var.num_amplify_variables
            value_list.append(var.decode(amplify_value_vector[start:stop]))
        return value_list

    def value_to_idx(self, value_list: list[Any]) -> list[int]:
        """Convert values of the variable list to value indices.

        Args:
            value_list (list[Any]): A list of the values to convert.

        Raises:
            RuntimeError: If `"amplify"` is specified as the encoding method.

        Returns:
            list[int]: The resulting value index list.
        """
        if self.method == AMPLIFY:
            raise RuntimeError("This method should not be necessary when Amplify SDK does the encoding.")

        idx_list: list[int] = []
        for i, var in enumerate(self._variable_list):
            idx_list.append(var.value_to_idx(value_list[i]))
        return idx_list

    def idx_to_value(self, idx_list: list[int]) -> list[Any]:
        """Convert value indices to values of the variable list.

        Args:
            idx_list (list[int]): A list of the value indices.

        Raises:
            RuntimeError: If `"amplify"` is specified as the encoding method.

        Returns:
            list[Any]: A list of the resulting values of the variable list.
        """
        if self.method == AMPLIFY:
            raise RuntimeError("This method should not be necessary when Amplify SDK does the encoding.")

        value_list: list[self.type] = []  # type: ignore
        for i, var in enumerate(self._variable_list):
            value_list.append(var.idx_to_value(idx_list[i]))
        return value_list

    def to_amplify_poly(self) -> amplify.Poly:
        """Convert the variable to a Amplify SDK's polynomial. The sum of all variables in the list is considered.

        Returns:
            amplify.Poly: The resulting polynomials.
        """
        ret = amplify.Poly()
        for var in self._variable_list:
            ret += var.to_amplify_poly()
        return ret

    def issue_amplify_variable(
        self,
        generator: amplify.VariableGenerator,
        var_counter: dict[amplify.VariableType, int],
        var_name: dict[amplify.VariableType, str],
    ) -> None:
        """Issue the Amplify SDK variables (`amplify.PolyArray`) relevant to the variables contained in this variable list, only when `VariableListBase.poly_array is None`.

        Args:
            generator (amplify.VariableGenerator): A variable generator.
            var_counter (dict[amplify.VariableType, int]): Counter counts how many amplify variables of each amplify.VariableType are issued.
            var_name (dict[amplify.VariableType, str]): Name prefix of amplify variables of each amplify.VariableType.
        """  # noqa: E501
        if self.poly_array is None:
            poly_array: list[amplify.Poly] = []
            for var in self.variable_list:
                var.issue_amplify_variable_impl(generator, var_counter, var_name)
                assert var.poly_array is not None
                poly_array += var.poly_array.to_list()
            self._poly_array = amplify.PolyArray(poly_array)

    def binary_to_idx(self, binary: list[int]) -> list[int]:
        """Convert a Amplify SDK's variable value vector (i.e. binary variable) to value indices of the variable list.

        Args:
            binary (list[int]): The Amplify SDK's variable value vector.

        Raises:
            RuntimeError: If `"amplify"` is specified as the encoding method.

        Returns:
            list[int]: A list of the resulting value indices of the variable list.
        """
        if self.method == AMPLIFY:
            raise RuntimeError("This method should not be necessary when the Amplify SDK does the encoding.")

        idx_list: list[int] = []
        for i, var in enumerate(self._variable_list):
            start = i * var.num_amplify_variables
            stop = start + var.num_amplify_variables
            idx_list.append(var.binary_to_idx(binary[start:stop]))
        return idx_list

    def idx_to_binary(self, idx_list: list[int]) -> list[int]:
        """Convert value indices of the variable array to a Amplify SDK's variable value vector.

        Args:
            idx_list (list[int]): A list of the value indices.

        Raises:
            RuntimeError: If `"amplify"` is specified as the encoding method.

        Returns:
            list[int]: The resulting Amplify SDK's variable value vector.
        """
        if self.method == AMPLIFY:
            raise RuntimeError("This method should not be necessary when Amplify SDK does the encoding.")

        binary: list[int] = []
        for i, var in enumerate(self._variable_list):
            binary += var.idx_to_binary(idx_list[i])
        return binary

    def generate_amplify_constraint(self) -> amplify.ConstraintList:
        """Generate the Amplify SDK's constraints related to the conversion of non-binary variable.

        Returns:
            amplify.ConstraintList: The resulting constraints.
        """
        constraints = amplify.ConstraintList()
        for var in self._variable_list:
            constraints += var.generate_amplify_constraint()
        return constraints

    def generate_random_value(
        self,
        rng: np.random.Generator,
        ref_value: list[Any] | None = None,
        find_neighbour: bool = False,
    ) -> Any:  # noqa: ANN401
        """Generate a random value compatible with the variable.

        If ref_value specified, only one element from ref_value
        is randomly modified so that values != ref_value. User-defined constraints (if there's any) are not considered
        in this value.

        Args:
            rng (np.random.Generator): NumPy's random generator.
            ref_value (list[Any] | None, optional): A list of reference values of the variable array. Defaults to `None`.
            find_neighbour (bool, optional): True to generate a random value neighbour to the reference value. Defaults to `False`.

        Returns:
            Any: A list of the resulting values of the variable array.
        """  # noqa: E501
        if ref_value is None:
            return [self[i].generate_random_value(rng) for i in range(self.len)]
        i_var = rng.integers(self.len)
        ref_value[i_var] = self[i_var].type(self[i_var].generate_random_value(rng, ref_value[i_var], find_neighbour))
        return ref_value

    def construct_discretize_table(self) -> np.ndarray:
        """Discretization information.

        Returns:
            np.ndarray: The variable list.
        """
        return self._variable_list[0].construct_discretize_table()

    def __str__(self) -> str:
        """Returns a human-readable information of the variables.

        Returns:
            str: The human-readable information of the variables.
        """
        df = pd.DataFrame(index=[], columns=[f"i={i}" for i in range(self.nbins)])
        df.loc[self.name] = self.construct_discretize_table()
        ret = print_to_str(
            pd.concat(
                [
                    pd.DataFrame(
                        [self.variable_list[0].type.__name__],
                        index=df.index,
                        columns=["type"],
                    ),
                    pd.DataFrame([self.variable_list[0].nbins], index=df.index, columns=["nbins"]),
                    pd.DataFrame([self.len], index=df.index, columns=["len"]),
                    pd.DataFrame(
                        [self.variable_list[0].method],
                        index=df.index,
                        columns=["method"],
                    ),
                    pd.DataFrame(
                        [self.variable_list[0].num_amplify_variables],
                        index=df.index,
                        columns=["nvars"],
                    ),
                    df,
                ],
                axis=1,
            )
        )
        return ret.removesuffix("\n")


@field
class BinaryVariable(VariableBase):
    """A class for the binary variable."""

    def __init__(self) -> None:
        """Constructor."""
        super().__init__(var_type=bool, bounds=(False, True), delta=0, nbins=1, method=None)

    def value_to_idx(self, value: bool) -> int:
        """Converts a value of the variable to a value index.

        Only for :obj:`BinaryVariable`, `value == idx == binary[0]`.

        Args:
            value (bool): The value to convert.

        Returns:
            int: The resulting value index.
        """
        return int(value)

    def idx_to_value(self, idx: int) -> bool:
        """Converts a value index to a value of the variable.

        Only for :obj:`BinaryVariable`, `value == idx == binary[0]`.

        Args:
            idx (int): The value index.

        Returns:
            bool: The resulting value.
        """
        return bool(idx)

    def to_amplify_poly(self) -> amplify.Poly:
        """Converts the variable to the Amplify SDK's polynomial.

        Raises:
            RuntimeError: If poly_array is not set for the variable.

        Returns:
            amplify.Poly: The resulting polynomial.
        """
        if self._poly_array is None:
            raise RuntimeError("poly array must be set for the variable.")
        return self._poly_array[0]

    def issue_amplify_variable_impl(
        self,
        generator: amplify.VariableGenerator,
        var_counter: dict[amplify.VariableType, int],
        var_name: dict[amplify.VariableType, str],
    ) -> None:
        """Issue the Amplify SDK variables relevant to this variable."""
        vtype = amplify.VariableType.Binary
        vname = f"{var_name[vtype]}{var_counter[vtype]}"
        self._poly_array = generator.array(vtype, 1, name=vname)
        var_counter[vtype] += 1

    def binary_to_idx(self, binary: list[int]) -> int:
        """Converts binary to value index. Only for :obj:`BinaryVariable`, `value == idx == binary[0]`. Note that returned binary from Amplify AE is `list[float]`, hence the `int()`.

        Args:
            binary (list[int]): The binary value

        Returns:
            int: The resulting index
        """  # noqa: E501
        return int(binary[0])

    def idx_to_binary(self, idx: int) -> list[int]:
        """Converts a value index to a binary vector.

        Args:
            idx (int): The value index.

        Returns:
            list[int]: The binary vector.
        """
        return [idx]


@field
class BinaryVariableList(VariableListBase):
    """A class for the binary variable array."""

    def __init__(self, length: int) -> None:
        """Constructor.

        Args:
            length (int): Length of the variable array.
        """
        super().__init__(
            var_type=bool,
            bounds=(False, True),
            delta=0,
            nbins=1,
            length=length,
            method=None,
        )
        self._variable_list = [BinaryVariable() for i in range(length)]


@field
class IntegerVariable(VariableBase):
    """A class for the integer variable."""

    def __init__(self, bounds: tuple, method: str = DOMAIN_WALL) -> None:
        """Constructor.

        Args:
            bounds (tuple): The lower and upper bounds that the variable can take.
            method (str, optional): Encoding method. 'dw': domain-wall. 'one_hot': one-hot. 'amplify': Amplify SDK's
            encoder. Defaults to 'dw'.
        """
        nbins = bounds[1] - bounds[0] + 1
        if method == AMPLIFY:
            nbins = 1
        super().__init__(var_type=int, bounds=bounds, delta=1, nbins=nbins, method=method)

    def value_to_idx(self, value: int) -> int:
        """Converts avalue of the variable to a value index.

        Args:
            value (int): The value to convert.

        Raises:
            RuntimeError: If 'amplify' is specified as the encoding method.
            ValueError: If the given value is out of range of (vmin, vmax).

        Returns:
            int: The resulting value  index.
        """
        if self.method == AMPLIFY:
            raise RuntimeError("This method should not be necessary when Amplify SDK does the encoding.")

        if value < self.bounds[0] or value > self.bounds[1]:
            raise ValueError(f"Given value {value} must be bounded by bounds={self.bounds}.")
        return value - self.bounds[0]

    def idx_to_value(self, idx: int) -> int:
        """Converts a value index to a value of the variable.

        Args:
            idx (int): The value index.

        Raises:
            RuntimeError: If 'amplify' is specified as the encoding method.

        Returns:
            int: The resulting value of the variable.
        """
        if self.method == AMPLIFY:
            raise RuntimeError("This method should not be necessary when Amplify SDK does the encoding.")

        return idx + self.bounds[0]

    def to_amplify_poly(self) -> amplify.Poly:
        """Converts the variable to the Amplify's polynomial.

        Raises:
            RuntimeError: If poly_array is not set for the variable.

        Returns:
            amplify.Poly: The resulting polynomial.
        """
        if self._poly_array is None:
            raise RuntimeError("poly array must be set for the variable.")

        if self.method == AMPLIFY:
            return self._poly_array[0]
        return self.idx_to_value(self.binary_to_idx(self._poly_array))  # type: ignore

    def issue_amplify_variable_impl(
        self,
        generator: amplify.VariableGenerator,
        var_counter: dict[amplify.VariableType, int],
        var_name: dict[amplify.VariableType, str],
    ) -> None:
        """Issue the Amplify SDK variables relevant to this variable."""
        if self.method == AMPLIFY:
            vtype = amplify.VariableType.Integer
            vname = f"{var_name[vtype]}{var_counter[vtype]}"
            self._poly_array = generator.array(vtype, 1, self.bounds, name=vname)
        else:
            vtype = amplify.VariableType.Binary
            vname = f"{var_name[vtype]}{var_counter[vtype]}"
            self._poly_array = generator.array(vtype, self.num_amplify_variables, name=vname)
        var_counter[vtype] += 1


@field
class IntegerVariableList(VariableListBase):
    """A class for the integer variable array."""

    def __init__(self, bounds: tuple, length: int, method: str = DOMAIN_WALL) -> None:
        """Constructor.

        Args:
            bounds (tuple): The lower and upper bounds that the variable can take.
            length (int): The length of the array.
            method (str, optional): Encoding method. 'dw': domain-wall. 'one_hot': one-hot. 'amplify': Amplify SDK's
            encoder. Defaults to 'dw'.
        """
        nbins = bounds[1] - bounds[0] + 1
        if method == AMPLIFY:
            nbins = 1
        super().__init__(
            var_type=int,
            bounds=bounds,
            delta=1,
            nbins=nbins,
            length=length,
            method=method,
        )
        self._variable_list = [IntegerVariable(self.bounds, method) for _ in range(self.len)]


@field
class RealVariable(VariableBase):
    """A class for the real variable with uniform discretization."""

    def __init__(self, bounds: tuple, nbins: int, method: str = DOMAIN_WALL) -> None:
        """Constructor.

        Args:
            bounds (tuple): The lower and upper bounds that the variable can take.
            nbins (int): The number of distretization points.
            method (str, optional): Encoding method. 'dw': domain-wall. 'one_hot': one-hot. 'amplify' is not available
            as of now. Defaults to 'dw'.

        Raises:
            ValueError: If 'amplify' is specified as the method.
            ValueError: If nbins is less than 2.
        """
        if method == AMPLIFY:
            raise ValueError(f"{self.__class__.__name__} cannot be used with the Amplify SDK encoding for now...")

        if nbins <= 1:
            raise ValueError(f"nbins must be greater than 1. {nbins=}")
        delta = float(bounds[1] - bounds[0]) / (nbins - 1)

        super().__init__(var_type=float, bounds=bounds, delta=delta, nbins=nbins, method=method)

    def value_to_idx(self, value: float) -> int:
        """Converts a value of the variable to a value index.

        Args:
            value (float): The value to convert.

        Raises:
            ValueError: If the given value if out of range of (vmin, vmax).

        Returns:
            int: The resulting value index.
        """
        if value < self.bounds[0] or value > self.bounds[1]:
            raise ValueError(f"Given value {value} must be bounded by bounds={self.bounds}.")
        return int((value - self.bounds[0]) / self.delta + 0.5)

    def idx_to_value(self, idx: int) -> float:
        """Converts a value index to a value of the variable.

        Args:
            idx (int): The value index.

        Returns:
            float: The resulting value of the variable.
        """
        return self.delta * idx + self.bounds[0]

    def to_amplify_poly(self) -> amplify.Poly:
        """Converts the variable to the Amplify's polynomial.

        Raises:
            RuntimeError: If the poly_array is not set for the variable.

        Returns:
            amplify.Poly: The resulting polynomial.
        """
        if self._poly_array is None:
            raise RuntimeError("poly array must be set for the variable.")

        return self.idx_to_value(self.binary_to_idx(self._poly_array))  # type: ignore

    def issue_amplify_variable_impl(
        self,
        generator: amplify.VariableGenerator,
        var_counter: dict[amplify.VariableType, int],
        var_name: dict[amplify.VariableType, str],
    ) -> None:
        """Issue the Amplify SDK variables relevant to this variable.

        Raises:
            RuntimeError: If the encoding method 'amplify' is used for RealVariable.

        """
        if self.method == AMPLIFY:
            raise RuntimeError("Encoding method 'amplify' cannot be used for RealVariable for now...")
        vtype = amplify.VariableType.Binary
        vname = f"{var_name[vtype]}{var_counter[vtype]}"
        self._poly_array = generator.array(vtype, self.num_amplify_variables, name=vname)
        var_counter[vtype] += 1


@field
class RealVariableList(VariableListBase):
    """A class for the real variable array with uniform discretization."""

    def __init__(
        self,
        bounds: tuple[float, float],
        nbins: int,
        length: int,
        method: str = DOMAIN_WALL,
    ) -> None:
        """Constructor.

        Args:
            bounds (tuple): The lower and upper bounds that the variable can take.
            nbins (int): The number of distretization points.
            length (int): The length of the array.
            method (str, optional): Encoding method. 'dw': domain-wall. 'one_hot': one-hot.
            'amplify' is not available as of now. Defaults to 'dw'.

        Raises:
            ValueError: If 'amplify' is specified as the method.
            ValueError: If nbins is less than 2.
        """
        if method == AMPLIFY:
            raise ValueError(f"{self.__class__.__name__} cannot be used with the Amplify SDK encoding for now...")

        if nbins <= 1:
            raise ValueError(f"nbins must be greater than 1. {nbins=}")
        delta = (bounds[1] - bounds[0]) / float(nbins - 1)

        super().__init__(
            var_type=float,
            bounds=bounds,
            delta=delta,
            nbins=nbins,
            length=length,
            method=method,
        )

        assert self.method is not None
        self._variable_list = [RealVariable(self.bounds, self.nbins, self.method) for _ in range(self.len)]


@field
class RealVariableLogUniform(VariableBase):
    """A class for the real variable with log-uniform discretization.

    value = min * delta^idx
    delta = (max / min)**(1 / (nbins - 1))
    """

    def __init__(self, bounds: tuple, nbins: int = 10, method: str = DOMAIN_WALL) -> None:
        """Constructor.

        Args:
            bounds (tuple): The lower and upper bounds that the variable can take.
            nbins (int, optional): The number of distretization points.. Defaults to 10.
            method (str, optional): Encoding method. 'dw': domain-wall. 'one_hot': one-hot. 'amplify' is not available
            as of now. Defaults to 'dw'.

        Raises:
            ValueError: If 'amplify' is specified as the method.
            ValueError: If nbins is less than 2.
            ValueError: If vmin * vmax <= 0.
        """
        if method == AMPLIFY:
            raise ValueError(f"{self.__class__.__name__} cannot be used with the Amplify SDK encoding.")

        if nbins <= 1:
            raise ValueError(f"nbins must be greater than 1. {nbins=}")

        if bounds[0] * bounds[1] <= 0:
            raise ValueError(
                f"the lower and upper bounds must be non-zero and the same sign for RealVariableLogUniform. {bounds=}."
            )

        delta = (bounds[1] / bounds[0]) ** (1.0 / (nbins - 1))

        super().__init__(var_type=float, bounds=bounds, delta=delta, nbins=nbins, method=method)

        self.epsilon = min(self.bounds[0], self.delta) / 1.0e6  # 1.0e6 for no reason. Just needs to be large enough.
        self._decimals = int(max(-math.log10(self.epsilon), 1.0))

        self._discretized_list = [
            np.round(self.bounds[0] * self.delta**idx, decimals=self._decimals) for idx in range(self.nbins)
        ]  # to account the rouding error

        self._incremental_list = [
            self._discretized_list[idx + 1] - self._discretized_list[idx] for idx in range(self.nbins - 1)
        ]

    @property
    def discretized_list(self) -> list:
        """Discretization list.

        Returns:
            list: Discretization list.
        """
        return self._discretized_list

    def value_to_idx(self, value: float) -> int:
        """Converts a value of the variable to a value index.

        Args:
            value (float): The value to convert.

        Raises:
            ValueError: If value < var_min.
            ValueError: value > var_max + epsilon.

        Returns:
            int: The resulting value index.
        """
        if value < self.bounds[0]:
            raise ValueError(f"Given value {value} must be >= {self.bounds[0]}.")
        if value > self.bounds[1] + self.epsilon:
            raise ValueError(f"Given value {value} must be <= {self.bounds[1]}.")
        return int(math.log(value / self.bounds[0], self.delta) + 0.5)

    def idx_to_value(self, idx: int) -> float:
        """Converts a value index to a value.

        Args:
            idx (int): The value index.

        Returns:
            float: The resulting value of the variable.
        """
        return self._discretized_list[idx]

    def to_amplify_poly(self) -> amplify.Poly:
        """Converts the variable to the Amplify's polynomial.

        Raises:
            RuntimeError: If the poly_array is not set for the variable.

        Returns:
            amplify.Poly: The resulting polynomial.
        """
        if self._poly_array is None:
            raise RuntimeError("poly array must be set for the variable.")

        if self.method == ONEHOT:
            return (self._poly_array * np.array(self._discretized_list)).sum()
        # Domain wall
        return self.bounds[0] + (self._poly_array * np.array(self._incremental_list)).sum()

    def issue_amplify_variable_impl(
        self,
        generator: amplify.VariableGenerator,
        var_counter: dict[amplify.VariableType, int],
        var_name: dict[amplify.VariableType, str],
    ) -> None:
        """Issue the Amplify SDK variables relevant to this variable.

        Raises:
            RuntimeError: If the encoding method 'amplify' is used for RealVariableLogUniform.
        """
        if self.method == AMPLIFY:
            raise RuntimeError("Encoding method 'amplify' cannot be used for RealVariableLogUniform for now...")
        vtype = amplify.VariableType.Binary
        vname = f"{var_name[vtype]}{var_counter[vtype]}"
        self._poly_array = generator.array(vtype, self.num_amplify_variables, name=vname)
        var_counter[vtype] += 1


@field
class RealVariableListLogUniform(VariableListBase):
    """A class for the real variable array with uniform discretization."""

    def __init__(
        self,
        bounds: tuple,
        nbins: int,
        length: int,
        method: str = DOMAIN_WALL,
    ) -> None:
        """Constructor.

        Args:
            bounds (tuple): The lower and upper bounds that the variable can take.
            nbins (int, optional): The number of distretization points.. Defaults to 10.
            length (int): The length of the array
            method (str, optional): Encoding method. 'dw': domain-wall. 'one_hot': one-hot. 'amplify' is not available
            as of now. Defaults to 'dw'.

        Raises:
            ValueError: If 'amplify' is specified as the method.
            ValueError: If nbins is less than 2.
            ValueError: If vmin * vmax <= 0.
        """
        if method == AMPLIFY:
            raise ValueError(f"{self.__class__.__name__} cannot be used with the Amplify SDK encoding.")

        if nbins <= 1:
            raise ValueError(f"nbins must be greater than 1. {nbins=}")

        if bounds[0] * bounds[1] <= 0:
            raise ValueError(
                f"the lower and upper must be non-zero and the same sign for RealVariableLogUniform. {bounds=}."
            )

        delta = (bounds[1] / bounds[0]) ** (1.0 / (nbins - 1))

        super().__init__(
            var_type=float,
            bounds=bounds,
            delta=delta,
            nbins=nbins,
            length=length,
            method=method,
        )

        assert self.method is not None
        self._variable_list = [RealVariableLogUniform(self.bounds, self.nbins, self.method) for _ in range(self.len)]


@field
class DiscreteVariable(VariableBase):
    """A class for the variable of an arbitrary type with arbitrary discretization defined by users."""

    def __init__(self, discretized_list: list[Any], method: str = DOMAIN_WALL) -> None:
        """Constructor.

        Args:
            discretized_list (list[Any]): A list of discretized values.
            method (str, optional): Encoding method. 'dw': domain-wall. 'one_hot': one-hot. 'amplify' is not available
            as of now. Defaults to 'dw'.

        Raises:
            ValueError: If 'amplify' is specified as the encoding method.
            ValueError: If the length of the discretized_list is less than 2.
            ValueError: If different types exists in the discretized_list.
            ValueError: If the discretized_list has duplicate elements.
        """
        if method == AMPLIFY:
            raise ValueError(f"{self.__class__.__name__} cannot be used with the Amplify SDK encoding.")

        if len(discretized_list) <= 1:
            raise ValueError(f"len(discretized_list) should be greater than 1. {len(discretized_list)=}")

        if discretized_list != sorted(discretized_list):
            logger().warning(f"discretized_list is not in ascending order. {discretized_list=}")

        unique_types = {type(element) for element in discretized_list}
        if len(unique_types) == 1:
            var_type = unique_types.pop()
        else:
            raise ValueError(
                f"elements in discretized_list have different types. {[type(x) for x in discretized_list]=}"
            )

        if var_type not in {bool, int, float}:
            raise ValueError(f"elements in discretized_list must be bool, int or float, but not {var_type}")

        if len(discretized_list) != len(set(discretized_list)):
            logger().warning(f"discretized_list has duplicate elements. {discretized_list=}")

        self._discretized_list = copy.deepcopy(discretized_list)  # potentially a variable can be a list

        super().__init__(
            var_type=var_type,
            bounds=(min(discretized_list), max(discretized_list)),
            delta=0.0,
            nbins=len(discretized_list),
            method=method,
        )

        self._incremental_list = [discretized_list[idx + 1] - discretized_list[idx] for idx in range(self.nbins - 1)]

    @property
    def discretized_list(self) -> list:
        """Discretization list.

        Returns:
            list: Discretization list.
        """
        return self._discretized_list

    @property
    def incremental_list(self) -> list[Any]:
        return self._incremental_list

    def value_to_idx(self, value: Any) -> int:  # noqa: ANN401
        """Converts a value of the variable to a value index.

        Args:
            value (Any): The value to convert.

        Raises:
            ValueError: If the value is not found in the discretized_list.

        Returns:
            int: The resulting value index.
        """
        if value in self._discretized_list:
            return self._discretized_list.index(value)
        raise ValueError(f"Given value {value} is not found in {self._discretized_list}.")

    def idx_to_value(self, idx: int) -> Any:  # noqa: ANN401
        """Converts a value index to a value of the variable.

        Args:
            idx (int): The value index.

        Returns:
            Any: The resulting value of the variable.
        """
        return self._discretized_list[idx]

    def to_amplify_poly(self) -> amplify.Poly:
        """Converts the variable to the Amplify's polynomial.

        Raises:
            RuntimeError: If poly_array is not set for the variable.

        Returns:
            amplify.Poly: The resulting polynomial.
        """
        if self._poly_array is None:
            raise RuntimeError("poly array must be set for the variable.")

        if self.method == ONEHOT:
            return (self._poly_array * np.array(self._discretized_list)).sum()
        # Domain  wall
        return self.bounds[0] + (self._poly_array * np.array(self.incremental_list)).sum()

    def issue_amplify_variable_impl(
        self,
        generator: amplify.VariableGenerator,
        var_counter: dict[amplify.VariableType, int],
        var_name: dict[amplify.VariableType, str],
    ) -> None:
        """Issue the Amplify SDK variables relevant to this variable.

        Args:
            generator (amplify.VariableGenerator): A variable generator instantiated by the Amplify SDK.
            var_counter (dict[amplify.VariableType, int]): Counters to count the number of variables of each variable type.
            var_name (dict[amplify.VariableType, str]): _description_

        Raises:
            RuntimeError: If the encoding 'amplify' is used for DiscreteVariable.
        """  # noqa: E501
        if self.method == AMPLIFY:
            raise RuntimeError("Encoding method 'amplify' cannot be used for DiscreteVariable for now...")
        vtype = amplify.VariableType.Binary
        vname = f"{var_name[vtype]}{var_counter[vtype]}"
        self._poly_array = generator.array(vtype, self.num_amplify_variables, name=vname)
        var_counter[vtype] += 1


@field
class DiscreteVariableList(VariableListBase):
    """A class for the real variable array with uniform discretization."""

    def __init__(self, discretized_list: list[Any], length: int, method: str = DOMAIN_WALL) -> None:
        """Constructor.

        Args:
            discretized_list (list[Any]): A list of discretized values.
            length (int): The length of the array.
            method (str, optional): Encoding method. 'dw': domain-wall. 'one_hot': one-hot. 'amplify' is not available
            as of now. Defaults to 'dw'.

        Raises:
            ValueError: If 'amplify' s specified as the encoding method.
        """
        if method == AMPLIFY:
            raise ValueError(f"{self.__class__.__name__} cannot be used with the Amplify SDK encoding.")

        unique_types = set(discretized_list)
        var_type = unique_types.pop()

        super().__init__(
            var_type=var_type,
            bounds=(min(discretized_list), max(discretized_list)),
            delta=0.0,
            nbins=len(discretized_list),
            length=length,
            method=method,
        )

        self._variable_list = [DiscreteVariable(discretized_list, self.method) for _ in range(self.len)]  # type: ignore
        self._variable_list = [DiscreteVariable(discretized_list, self.method) for _ in range(self.len)]  # type: ignore
        self._variable_list = [DiscreteVariable(discretized_list, self.method) for _ in range(self.len)]  # type: ignore
