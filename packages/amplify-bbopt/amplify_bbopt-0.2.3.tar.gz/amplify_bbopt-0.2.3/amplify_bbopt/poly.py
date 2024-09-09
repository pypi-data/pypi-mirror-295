# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

import copy
from typing import TYPE_CHECKING, Any

import amplify

if TYPE_CHECKING:
    from .variable import Variable

# Encoding method
DOMAIN_WALL = "dw"  # default
ONEHOT = "one_hot"
# Amplify SDK handles variable encoding with "default" (FM can consider non-binary variables)
AMPLIFY = "amplify"


class Poly:
    """Class to define polynomial of the variables."""

    def __init__(self, terms: dict[Variable, float] | None = None) -> None:
        """Initialize a polynomial.

        Args:
            terms (dict[Variable, float] | None, optional): A dictionary of variables and their coefficients. Defaults to `None`.
        """  # noqa: E501
        if terms is None:
            self.terms = {}
        else:
            self.terms = terms

    def __add__(self, other: Any) -> Poly:  # noqa: ANN401
        """Perform addition between two polynomials or a polynomial class and a variable (list).

        Args:
            other: An instance of the :obj:`Poly` class or a variable (list) class.

        Returns:
            Poly: The final polynomials.
        """
        # Could use isinstance(other, VariableBase), but this enforces an unresolvable circular import
        if hasattr(other, "to_poly"):
            other = other.to_poly()
        result = copy.copy(self.terms)
        for k, v in other.terms.items():
            if k in result:
                result[k] += v
            else:
                result[k] = v
        return Poly(result)

    def __sub__(self, other: Any) -> Poly:  # noqa: ANN401
        """Perform subtraction between two polynomials or a polynomial class and a variable (list).

        Args:
            other: An instance of the :obj:`Poly` class or a variable (list) class.

        Returns:
            Poly: The final polynomials.
        """
        # Could use isinstance(other, VariableBase), but this enforces an unresolvable circular import
        if hasattr(other, "to_poly"):
            other = other.to_poly()
        result = copy.copy(self.terms)
        for k, v in other.terms.items():
            if k in result:
                result[k] -= v
            else:
                result[k] = -v
        return Poly(result)

    def to_amplify_poly(self) -> amplify.Poly:
        """Convert the polynomial to an Amplify SDK compatible polynomial.

        Returns:
            amplify.Poly: The constructed Amplify SDK's polynomial.
        """
        ret = amplify.Poly()
        for variable, factor in self.terms.items():
            ret += variable.to_amplify_poly() * factor
        return ret
