# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import numpy as np


def sphere_function(x: list[float]) -> float:
    """An example objective function (sphere function). Yield the global minimum of 0 at (0, 0, ...).

    Args:
        x (list[float]): An input vector.

    Returns:
        float: The function value.
    """
    return (np.array(x) ** 2).sum()


def goldstein_price_function(x0: float, x1: float) -> float:
    """An example objective function (Goldstein-Price function). Yield the global minimum of 3 at (0, -1).

    Args:
        x0 (float): A real number
        x1 (float): A real number

    Returns:
        float: The function value.
    """
    return (1 + (x0 + x1 + 1) ** 2 * (19 - 14 * x0 + 3 * x0 * x0 - 14 * x1 + 6 * x0 * x1 + 3 * x1 * x1)) * (
        30 + ((2 * x0 - 3 * x1) ** 2) * (18 - 32 * x0 + 12 * x0 * x0 + 48 * x1 - 36 * x0 * x1 + 27 * x1 * x1)
    )


def rosenbrock_function(x: list[float]) -> float:
    """An example objective function (Rosenbrock function). Yield the global minimum of 0 at (1, 1, ...).

    Args:
        x (list[float]): An input vector.

    Returns:
        float: The function value.
    """
    assert len(x) > 1
    return ((1 - np.array(x)[:-1]) ** 2 + 100 * (np.array(x)[1:] - np.array(x)[:-1] ** 2) ** 2).sum()


def rastrigin_function(x: list[float]) -> float:
    """An example objective function (Rastrigin function). Yield the global minimum of 0 at (0, 0, ...).

    Args:
        x (list[float]): An input vector.

    Returns:
        float: The function value.
    """
    return 10 * len(x) + (np.array(x) ** 2 - 10 * np.cos(2 * np.pi * np.array(x))).sum()
