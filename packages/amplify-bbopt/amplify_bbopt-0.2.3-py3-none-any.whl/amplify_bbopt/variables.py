# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

import itertools

import amplify
import numpy as np
import pandas as pd

from .misc import print_to_str
from .solution_type import StructuredSolution, StructuredSolutionDict
from .variable import VariableBase, VariableListBase

pd.set_option("display.max_columns", 500)
pd.set_option("display.width", 1000)


class Variables:
    """A class for variables with different types."""

    def __init__(self, **kwargs: VariableBase | VariableListBase) -> None:
        """Constructor."""
        self.var_dict: dict[str, VariableBase | VariableListBase] = {}

        # number of instances of VariableBase and VariableBase in the VariableListBase
        self._num_elemental_variables = 0

        # number of the Amplify SDK's variables.
        self._num_amplify_variables = 0

        for k, v in kwargs.items():
            self._set_variable(k, v)

        self._variable_generator = amplify.VariableGenerator()
        self._poly_array: amplify.PolyArray | None = None

        self._variable_counter = {
            amplify.VariableType.Binary: 0,
            amplify.VariableType.Integer: 0,
            amplify.VariableType.Real: 0,
        }
        self._variable_name = {
            amplify.VariableType.Binary: "q",
            amplify.VariableType.Integer: "n",
            amplify.VariableType.Real: "x",
        }

    @property
    def variable_generator(self) -> amplify.VariableGenerator:
        """The Amplify SDK's variable generator."""
        return self._variable_generator

    @variable_generator.setter
    def variable_generator(self, value: amplify.VariableGenerator) -> None:
        self._variable_generator = value

    def unify_variables(
        self,
        var_dict_universe: dict[str, VariableBase | VariableListBase],
        variable_generator: amplify.VariableGenerator,
    ) -> None:
        """Unify duplicate variables in different :obj:`Variables` class instances associated with this :obj:`BlackBoxFuncList` class.

        Args:
            var_dict_universe (dict[str, VariableBase  |  VariableListBase]): A variable dictionary containing all the variables with their names in the multiple :obj:`Variables` class instances.
            variable_generator (amplify.VariableGenerator): A variable generator instantiated in the Amplify SDK.

        Raises:
            RuntimeError: If unknown variable name is found.
        """  # noqa: E501
        self.variable_generator = variable_generator
        for k in self.var_dict:
            if k not in var_dict_universe:
                raise RuntimeError(f"the variable {k} was not found.")
            # Unify duplicate variables.
            self.var_dict[k] = var_dict_universe[k]
            # Try to issue amplify.PolyArray (if already exists, done nothing)
            self.var_dict[k].issue_amplify_variable(
                self.variable_generator, self._variable_counter, self._variable_name
            )
        self.set_elemental_poly_array()

    def issue_amplify_variable(self) -> None:
        """Issue the Amplify SDK's variables (:obj:`amplify.PolyArray`) for all elemental variables."""
        for var in self.var_dict.values():
            var.issue_amplify_variable(self._variable_generator, self._variable_counter, self._variable_name)

    def set_elemental_poly_array(self) -> None:
        """Set :obj:`amplify.PolyArray` (issued in :obj:`Variables.issue_amplify_variable`) of all elemental variables to :obj:`Variables.poly_array`.

        Raises:
            RuntimeError: If poly_array is not set for the variable.

        """  # noqa: E501
        poly_list: list[amplify.Poly] = []
        for var in self.var_dict.values():
            if isinstance(var, VariableListBase):
                for v in var:
                    assert v.poly_array is not None
                    poly_list += v.poly_array.to_list()
            else:
                if var.poly_array is None:
                    raise RuntimeError("VariableBase.poly_array is not set.")
                poly_list += var.poly_array.to_list()
        self._poly_array = amplify.PolyArray(poly_list)

    @property
    def num_elemental_variables(self) -> int:
        """A number of instances of :obj:`VariableBase` and :obj:`VariableBase` in the :obj:`VariableListBase` instances."""  # noqa: E501
        return self._num_elemental_variables

    @property
    def num_amplify_variables(self) -> int:
        """A number of encoded variables for [:obj:`num_elemental_variables`] variables."""
        return self._num_amplify_variables

    def __len__(self) -> int:
        return len(self.var_dict)

    def __getitem__(self, i: int) -> VariableBase | VariableListBase:
        return list(self.var_dict.values())[i]

    def __getattr__(self, name: str) -> VariableBase | VariableListBase:
        """Get a variable in var_dict.

        Args:
            name (str): The variable name.

        Raises:
            ValueError: If variable with a given name is not found.

        Returns:
            VariableBase | VariableListBase: A variable or variable list.
        """
        if name not in self.var_dict:
            raise ValueError(
                f"No such variable {name} is found in this Variables class instance. [{self.var_dict.keys()}]."
            )
        return self.var_dict[name]

    def _set_variable(self, name: str, var: VariableBase | VariableListBase) -> None:
        """Set variable with its name and index.

        Args:
            name (str): The variable name
            var (VariableBase | VariableListBase): The variable to set.
        """
        if name not in self.var_dict:
            self._num_elemental_variables += var.len
            self._num_amplify_variables += var.num_amplify_variables
        self.var_dict[name] = var
        self.var_dict[name].name = name
        if isinstance(var, VariableListBase):
            for i, v in enumerate(var):
                v.name = f"{name}[{i}]"

    def _del_variable(self, name: str) -> None:
        """Delete a variable.

        Args:
            name (str): The name of variable to delete.
        """
        del self.var_dict[name]

    def nullify_poly_array(self, vars_count: int = 0) -> None:
        """Make :obj:`poly_array = None` for all variables involved."""
        for var in self.var_dict.values():
            var.nullify_poly_array()
        self._poly_array = None
        self._variable_counter[amplify.VariableType.Binary] = 0
        self._variable_counter[amplify.VariableType.Integer] = 0
        self._variable_counter[amplify.VariableType.Real] = 0

        post_fix = ""
        for _i in range(vars_count):
            post_fix += "'"
        self._variable_name[amplify.VariableType.Binary] = "q" + post_fix
        self._variable_name[amplify.VariableType.Integer] = "n" + post_fix
        self._variable_name[amplify.VariableType.Real] = "x" + post_fix

    @property
    def poly_array(self) -> amplify.PolyArray:
        """The Amplify SDK's variables (:obj:`amplify.PolyArray`) that represents the variables in this :obj:`Variables`."""  # noqa: E501
        if self._poly_array is None:
            self.issue_amplify_variable()
            self.set_elemental_poly_array()
        assert self._poly_array is not None
        return self._poly_array

    @property
    def amplify_variables(self) -> dict[str, amplify.Poly | amplify.PolyArray]:
        """The Amplify SDK's variables (:obj:`amplify.PolyArray`) in dictionary form that represents the variables in this :obj:`Variables`."""  # noqa: E501
        # This assert MUST be for self.poly_array, not for self._poly_array.
        assert self.poly_array is not None
        return {v.name: v.poly_array for v in self.var_dict.values()}  # type: ignore

    def convert_to_amplify_solution_dict(
        self, solution_dict: StructuredSolutionDict
    ) -> dict[amplify.Poly, int | float]:
        """Convert from Amplify-BBOpt's solution dict to Amplify SDK's solution dict.

        Args:
            solution_dict (StructuredSolutionDict): Amplify-BBOpt's solution dict. This can be entire solution in case of multiple-objective optimization (keys other than this :obj:`Variables`' keys can exist in the solution dict).

        Returns:
            dict[amplify.Poly, int | float]: The converted Amplify SDK';'s solution dict.
        """  # noqa: E501
        ret: dict[amplify.Poly, int | float] = {}
        for k, v in solution_dict.items():
            encoded = self.var_dict[k].encode(v)  # type: ignore
            assert self.var_dict[k].poly_array is not None
            for i, poly in enumerate(self.var_dict[k].poly_array):  # type: ignore
                assert isinstance(poly, amplify.Poly)
                ret[poly] = encoded[i]
        return ret

    @property
    def names(self) -> list:
        """Return names of the variables.

        Returns:
            list: A list of the variable names.
        """
        return list(self.var_dict.keys())

    @property
    def flat_names(self) -> list[str]:
        """Return names of the variables. The variable names for a variable list is expanded.

        (the names of elemental variables in a variable list are returned instead of the name of the variable list).

        Raises:
            RuntimeError: If the variable name is not set.

        Returns:
            list: A list of the variable names in a 'flat' manner.
        """
        names: list[str] = []
        for var in self.var_dict.values():
            if isinstance(var, VariableListBase):
                var_names: list[str] = [v.name for v in var if v.name is not None]
                names += var_names
            else:
                if var.name is None:
                    raise RuntimeError("variable name is not set yet.")
                names.append(var.name)
        return names

    def __str__(self) -> str:
        """Return a human-readable information of the variables.

        Returns:
            str: The human-readable information of the variables.
        """
        nbins_max = max(var.nbins for var in self.var_dict.values())
        df = pd.DataFrame(index=[], columns=[f"i={i}" for i in range(nbins_max)])
        for key, var in self.var_dict.items():
            filler = np.full(nbins_max - var.nbins, "-")
            df.loc[key] = np.append(var.construct_discretize_table(), filler)

        ret = print_to_str(
            pd.concat(
                [
                    pd.DataFrame(
                        [var.type.__name__ for var in self.var_dict.values()],
                        index=df.index,
                        columns=["type"],
                    ),
                    pd.DataFrame(
                        [var.nbins for var in self.var_dict.values()],
                        index=df.index,
                        columns=["nbins"],
                    ),
                    pd.DataFrame(
                        [var.len for var in self.var_dict.values()],
                        index=df.index,
                        columns=["len"],
                    ),
                    pd.DataFrame(
                        [var.method for var in self.var_dict.values()],
                        index=df.index,
                        columns=["method"],
                    ),
                    pd.DataFrame(
                        [var.num_amplify_variables for var in self.var_dict.values()],
                        index=df.index,
                        columns=["nvars"],
                    ),
                    df,
                ],
                axis=1,
            )
        )
        return ret.removesuffix("\n")

    def encode(self, x: StructuredSolution) -> list[int | float]:
        """Encode an input value vector to an the Amplify SDK's variable value vector.

        Args:
            x (StructuredSolution): The input value vector.

        Raises:
            RuntimeError: If the length of the input value vector does not match with the number of variables.

        Returns:
            list[int | float]: A list of the resulting encoded value vector.
        """
        if len(self) != len(x.values):
            raise RuntimeError(f"{len(x.values)=} and len(variables)={len(self)} do not match.")
        encoded_values = [var.encode(x.values[i]) for i, var in enumerate(self.var_dict.values())]  # type: ignore
        return list(itertools.chain(*encoded_values))

    def decode(self, encoded_values: list[int | float]) -> StructuredSolution:
        """Decodes an encoded value vector to an input value vector.

        Args:
            encoded_values (list[int | float]): A primitive value vector (as in the Amplify SDK's variables).

        Raises:
            RuntimeError: The number of encoded variables does not match with the length of the encoded value vector.

        Returns:
            StructuredSolution: The resulting input value vector.
        """
        if self.num_amplify_variables != len(encoded_values):
            raise RuntimeError(
                f"{len(encoded_values)=} and num_amplify_variables={self.num_amplify_variables} do not match."
            )

        start = 0
        ret: list[bool | int | float | list[bool] | list[int] | list[float]] = []
        for var in self.var_dict.values():
            stop = start + var.num_amplify_variables
            ret.append(var.decode(encoded_values[start:stop]))
            start = stop

        return StructuredSolution(self, ret)

    def generate_random_value(
        self,
        rng: np.random.Generator,
        ref_value: StructuredSolution | None = None,
        find_neighbour: bool = False,
    ) -> StructuredSolution:
        """Generates random value vector compatible with self. If ref_value is specified, only one element in ref_value will be randomly modified so that the return value vector yields close values to the ref_value. Note that ref_value will not be modified.

        Args:
            rng (np.random.Generator): NumPy's random generator.
            ref_value (StructuredSolution | None, optional): A reference input value vector. Defaults to None.
            find_neighbour (bool, optional): True to generate a random value neighbour to the reference value. Defaults to `False`.

        Returns:
            StructuredSolution: The resulting input value vector of the variables.
        """  # noqa: E501
        if ref_value is None:
            return StructuredSolution(self, [v.generate_random_value(rng) for v in self.var_dict.values()])
        value = ref_value.copy()
        idx_variable = rng.integers(len(self))
        variable_to_modify = list(self.var_dict.values())[idx_variable]
        value.values[idx_variable] = variable_to_modify.generate_random_value(
            rng,
            value.values[idx_variable],  # type: ignore
            find_neighbour,
        )
        return value

    def generate_amplify_constraint(self) -> amplify.ConstraintList:
        """Constructs one_hot/domain_wall constraints required for non-binary decision variables.

        Returns:
            amplify.ConstraintList: The resulting constraints.
        """
        constraints = amplify.ConstraintList()
        for var in self.var_dict.values():
            constraints += var.generate_amplify_constraint()
        return constraints
