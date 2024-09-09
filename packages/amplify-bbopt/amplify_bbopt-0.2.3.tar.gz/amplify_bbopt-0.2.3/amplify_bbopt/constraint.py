# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from typing import TYPE_CHECKING, Any

import amplify

from .misc import print_to_str, short_line
from .variable import Poly, Variable
from .variables import VariableListBase

if TYPE_CHECKING:
    from collections.abc import Iterator

    from .solution_type import FlatSolutionDict

EQ = "=="
LE = "<="
GE = ">="
CL = "cl"


def equal_to(left: Poly | VariableListBase, right: float) -> Constraint:
    """Construct a user-defined equality constraint that the given l.h.s. polynomial equals to the r.h.s. value.

    Args:
        left (Poly | VariableListBase): A polynomial of variables. If a 'variable list' is directly given, its sum is considered as the l.h.s. polynomial.
        right (float): R.h.s. value.

    Returns:
        Constraint: Constructed equality constraint.
    """  # noqa: E501
    return Constraint(left, EQ, right)


def less_equal(left: Poly | VariableListBase, right: float) -> Constraint:
    """Construct a user-defined inequality constraint that the given l.h.s. polynomial equals to or less than the r.h.s. value.

    Args:
        left (Poly | VariableListBase): A polynomial of variables. If a 'variable list' is directly given, its sum is considered as the l.h.s. polynomial.
        right (float): R.h.s. value.

    Returns:
        Constraint: Constructed inequality constraint.
    """  # noqa: E501
    return Constraint(left, LE, right)


def greater_equal(left: Poly | VariableListBase, right: float) -> Constraint:
    """Construct a user-defined inequality constraint that the given l.h.s. polynomial equals to or greater than the r.h.s. value.

    Args:
        left (Poly | VariableListBase): A polynomial of variables. If a 'variable list' is directly given, its sum is considered as the l.h.s. polynomial.
        right (float): R.h.s. value.

    Returns:
        Constraint: Constructed inequality constraint
    """  # noqa: E501
    return Constraint(left, GE, right)


def clamp(left: Poly | VariableListBase, right: tuple) -> Constraint:
    """Construct a user-defined inequality constraint that the given l.h.s. polynomial ranges between lower and upper bounds specified as r.h.s.

    Args:
        left (Poly | VariableListBase): A polynomial of variables. If a 'variable list' is directly given, its sum is considered as the l.h.s. polynomial.
        right (tuple): Lower and upper bounds of the range as r.h.s. vlaue.

    Raises:
        ValueError: If the lower bound value is greater than the upper bound value.

    Returns:
        Constraint: Constructed inequality constraint.
    """  # noqa: E501
    if right[0] > right[1]:
        raise ValueError(f"right[0] must be less than or equal to right[1], but {right} is given.")
    return Constraint(left, CL, right)


class Constraint:
    """A class for a user-defined constraint."""

    def __init__(self, left: Poly | VariableListBase, op: str, right: float | tuple) -> None:
        """Initialize constraint.

        Args:
            left (Poly | VariableListBase): A polynomial of variables. If a 'variable list' is directly given, its sum is considered as the l.h.s. polynomial.
            op (str): An equality or inequality operator of the constraint.
            right (float | tuple): R.h.s. value.
        """  # noqa: E501
        if isinstance(left, Poly):
            self._left = left
        else:
            self._left = left.sum()

        self._op = op
        self._right = right
        self._weight = 1.0
        self._penalty_formulation = "Default"

    def unify_variables(self, var_dict_universe: dict[str, Any]) -> None:
        """Unify duplicate variables used in the constraint and across different constraints. Intended for multi-objective optimizations where the same variable is used in different black-box objective functions. Calling this for single-objective optimization has no effect.

        Args:
            var_dict_universe (dict[str, Any]): A dictionary of all variable names and variables appearing in black-box functions. In the same form as :obj:`Variables.var_dict` (structured).
        """  # noqa: E501
        var_dict_elemental_universe: dict[str, Any] = {}
        for var in var_dict_universe.values():
            if isinstance(var, VariableListBase):
                for v in var:
                    assert v.name is not None
                    var_dict_elemental_universe[v.name] = v
            else:
                assert var.name is not None
                var_dict_elemental_universe[var.name] = var

        new_left_terms: dict[Variable, float] = {}
        for var, coef in self._left.terms.items():
            assert var.name is not None
            unified_var = var_dict_elemental_universe[var.name]
            new_left_terms[unified_var] = coef
        self._left = Poly(new_left_terms)

    @property
    def left(self) -> Poly:
        """A l.h.s. of the constraint (a polynomial of variables)."""
        return self._left

    @property
    def op(self) -> str:
        """An equality or inequality operator symbol of a constraint."""
        return self._op

    @property
    def right(self) -> int | float | tuple:
        """A r.h.s. value of the constraint."""
        return self._right

    @property
    def weight(self) -> float:
        """A constraint weight."""
        return self._weight

    @weight.setter
    def weight(self, value: float) -> None:
        """Set a constraint weight.

        Args:
            value (float): A constraint weight.
        """
        self._weight = value

    @property
    def penalty_formulation(self) -> str:
        """The Amplify SDK's `penalty_formulation` parameter.

        Set this to "Relaxation" when:

        (1) Imposing an inequality constraint with real variables (when coefficients in the constraint formulation is likely to yield real numbers), AND

        (2) The specified solver (e.g Amplify Annealing Engine) being a QUBO solver that does not support real variables,
        until the Amplify SDK used internally in Amplify-BBOpt supports the real-to-binary variable conversion. See: https://amplify.fixstars.com/ja/docs/amplify/v1/penalty.html#ineq-penalty
        """  # noqa: E501
        return self._penalty_formulation

    @penalty_formulation.setter
    def penalty_formulation(self, value: str) -> None:
        """Set the Amplify SDK's `penalty_formulation` parameter.

        Set this to "Relaxation" when:
        - Imposing an inequality constraint with real variables (when coefficients in the constraint formulation is likely to yield real numbers), AND
        - The specified solver (e.g Amplify Annealing Engine) being a QUBO solver that does not support real variables,
        until the Amplify SDK used internally in Amplify-BBOpt supports the real-to-binary variable conversion. See: https://amplify.fixstars.com/ja/docs/amplify/v1/penalty.html#ineq-penalty

        Args:
            value (float): A `penalty_formulation`.
        """  # noqa: E501
        self._penalty_formulation = value

    def to_amplify_constraint(self) -> amplify.Constraint:
        """Convert the constraint to the Amplify SDK's constraint.

        Raises:
            ValueError: If an operator is invalid.

        Returns:
            amplify.Constraint: A converted constraint.
        """
        poly = self.left.to_amplify_poly()
        if self.op == EQ:
            c = amplify.equal_to(poly, self.right)  # type: ignore
        elif self.op == LE:
            c = amplify.less_equal(poly, self.right, penalty_formulation=self._penalty_formulation)  # type: ignore
        elif self.op == GE:
            c = amplify.greater_equal(poly, self.right)  # type: ignore
        elif self.op == CL:
            c = amplify.clamp(poly, self.right)  # type: ignore
        else:
            raise ValueError(f"{self.op} is invalid keyword.")
        c.weight = self._weight
        return c

    def is_satisfied(self, solution_dict: FlatSolutionDict) -> bool:
        """Return whether a given input (solution of the optimization) meets the constraint.

        Args:
            solution_dict (FlatSolutionDict): A solution.

        Raises:
            ValueError: If a variable used in the constraint is not found in the `solution_dict` .
            ValueError: If an operator is invalid.

        Returns:
            bool: True if the constraint is met.
        """
        left_val = 0.0
        for variable, factor in self.left.terms.items():
            assert variable.name is not None
            if variable.name not in solution_dict:
                raise ValueError(
                    f"variable {variable.name} is not found in candidate variables {list(solution_dict.keys())}. In case of multiple-objective optimization, use BlackBoxFuncList."  # noqa: E501
                )
            left_val += factor * solution_dict[variable.name]

        if self.op == EQ:
            return left_val == self.right
        if self.op == LE:
            return left_val <= self.right  # type: ignore
        if self.op == GE:
            return left_val >= self.right  # type: ignore
        if self.op == CL:
            return self.right[0] <= left_val and left_val <= self.right[1]  # type: ignore
        raise ValueError(f"{self.op} is invalid keyword.")

    def __str__(self) -> str:
        """Return a human-readable constraint expression.

        Returns:
            str: A constraint expression.
        """
        poly_str = ""
        for variable, factor in self.left.terms.items():
            sign = "-"
            if factor > 0:
                sign = "+"
            abs_factor_str = ""
            if abs(factor) != 1:
                abs_factor_str = f"{abs(factor)} "
            poly_str = f"{poly_str} {sign} {abs_factor_str}{variable.name}"

        poly_str = poly_str.removeprefix(" + ").removeprefix(" ")

        if self.op != CL:
            return f"constraint: {poly_str} {self.op} {self.right}"

        return f"constraint: {self.right[0]} <= {poly_str} <= {self.right[1]}"  # type: ignore

    def __repr__(self) -> str:
        return str(self)


class Constraints:
    """Class for multiple constraints."""

    def __init__(self, c: Constraint | Constraints | list[Constraint | Constraints] | None = None) -> None:
        """Initialize the class from constraint(s) in different form.

        Args:
            c (Constraint | Constraints | list[Constraint | Constraints] | None, optional): Created constraints. If set `None` an empty :obj:`Constraints` will be created. Defaults to `None`.
        """  # noqa: E501
        self._constraint_list: list[Constraint] = []
        if c is None:
            return
        self.append(c)

    def __str__(self) -> str:
        """Return human-readable constraint expressions.

        Returns:
            str: Constraint expressions.
        """
        ret = print_to_str(short_line)
        for c in self._constraint_list:
            ret += print_to_str(f"{c} (weight: {c.weight})")
        return ret.removesuffix("\n")

    def __repr__(self) -> str:
        return str(self)

    def __len__(self) -> int:
        """Return a number of constraints in the class.

        Returns:
            int: A number of constraints in the class.
        """
        return len(self._constraint_list)

    def __iter__(self) -> Iterator[Constraint]:
        yield from self._constraint_list

    def append(
        self, c: Constraint | Constraints | list[Constraint | Constraints] | list[Constraint] | list[Constraints]
    ) -> None:
        """Add constraints to the class.

        Args:
            c (Constraint | Constraints | list[Constraint | Constraints] | list[Constraint] | list[Constraints]): Constraints.
        """  # noqa: E501

        def append_constraints(c: Constraints) -> None:
            for c_j in c:
                self._constraint_list.append(c_j)

        if isinstance(c, list):
            for c_i in c:
                if isinstance(c_i, Constraint):
                    self._constraint_list.append(c_i)
                else:
                    append_constraints(c_i)
        elif isinstance(c, Constraint):
            self._constraint_list.append(c)
        else:
            append_constraints(c)

    def to_amplify_constraint(self) -> amplify.ConstraintList:
        """Convert the constraints to the Amplify SDK's `ConstraintList`.

        Returns:
            amplify.ConstraintList: Converted constraints.
        """
        constraints = amplify.ConstraintList()
        for c in self._constraint_list:
            constraints += c.to_amplify_constraint()
        return constraints

    def is_satisfied(self, solution_dict: FlatSolutionDict) -> bool:
        """Return whether a given solution (input) meets all constraints.

        Args:
            solution_dict (FlatSolutionDict): A solution to evaluate.

        Returns:
            bool: True if all constraints are met.
        """
        is_satisfied = True
        for c in self:
            if not c.is_satisfied(solution_dict):
                is_satisfied = False
                break
        return is_satisfied

    def unify_variables(self, var_dict_universe: dict[str, Any]) -> None:
        """Unify duplicate variables used in the constraint and across different constraints. Intended for multi-objective optimizations where the same variable is used in different black-box objective functions. Calling this for single-objective optimization has no effect.

        Args:
            var_dict_universe (dict[str, Any]): A dictionary of all variable names and variables appearing in black-box functions. In the same form as :obj:`Variables.var_dict` (structured).
        """  # noqa: E501
        for c in self._constraint_list:
            c.unify_variables(var_dict_universe)
            c.unify_variables(var_dict_universe)
            c.unify_variables(var_dict_universe)
