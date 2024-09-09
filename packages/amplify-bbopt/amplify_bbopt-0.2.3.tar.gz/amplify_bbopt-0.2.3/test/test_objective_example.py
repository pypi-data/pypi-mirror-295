# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from amplify_bbopt.objective_example import (
    goldstein_price_function,
    rastrigin_function,
    rosenbrock_function,
    sphere_function,
)


def test_goldstein_price_function():
    assert goldstein_price_function(0, -1) == 3


def test_rosenbrock_function():
    assert rosenbrock_function([1, 1]) == 0
    assert rosenbrock_function([1, 1, 1]) == 0
    assert rosenbrock_function([1, 1, 1, 1]) == 0


def test_rastrigin_function():
    assert rastrigin_function([0, 0]) == 0
    assert rastrigin_function([0, 0, 0]) == 0
    assert rastrigin_function([0, 0, 0, 0]) == 0


def test_sphere_function():
    assert sphere_function([0, 0]) == 0
    assert sphere_function([0, 0, 0]) == 0
    assert sphere_function([0, 0, 0, 0]) == 0
