# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import amplify
import numpy as np
import pytest
from amplify_bbopt.variable import (
    BinaryVariable,
    BinaryVariableList,
    DiscreteVariable,
    DiscreteVariableList,
    IntegerVariable,
    IntegerVariableList,
    RealVariable,
    RealVariableList,
    RealVariableListLogUniform,
    RealVariableLogUniform,
    VariableListBase,
)

var_counter = {amplify.VariableType.Binary: 0, amplify.VariableType.Integer: 0, amplify.VariableType.Real: 0}
var_name = {amplify.VariableType.Binary: "q", amplify.VariableType.Integer: "n", amplify.VariableType.Real: "x"}


def test_discrete_domain():
    assert RealVariable(bounds=(0, 1), nbins=3).discrete_domain is None
    assert RealVariableLogUniform(bounds=(0.1, 1), nbins=3).discrete_domain is None
    assert RealVariableList(bounds=(0, 1), nbins=3, length=2).discrete_domain is None
    assert RealVariableListLogUniform(bounds=(0.1, 1), nbins=3, length=2).discrete_domain is None

    assert DiscreteVariable(discretized_list=[0.0, 0.5, 2.0]).discrete_domain == [0.0, 0.5, 2.0]
    assert DiscreteVariableList(discretized_list=[0.0, 0.5, 2.0], length=2).discrete_domain == [0.0, 0.5, 2.0]

    assert IntegerVariable(bounds=(0, 2)).discrete_domain == list(range(3))
    assert IntegerVariableList(bounds=(0, 2), length=2).discrete_domain == list(range(3))

    assert BinaryVariable().discrete_domain == [False, True]
    assert BinaryVariableList(length=2).discrete_domain == [False, True]


def test_real_variable_array():
    variable_array = RealVariableList(bounds=(-1.0, 1.0), nbins=5, length=2)
    assert variable_array.len == 2
    assert variable_array.num_amplify_variables == 8
    assert variable_array.encode([-1.0, 0.5]) == [0, 0, 0, 0, 1, 1, 1, 0]

    assert variable_array.decode([1, 1, 0, 0, 1, 1, 1, 1]) == [0.0, 1.0]
    assert isinstance(variable_array, VariableListBase)
    assert isinstance(variable_array[0], RealVariable)

    with pytest.raises(ValueError) as _:
        _ = RealVariableList(bounds=(-1.0, 1.0), nbins=5, length=1)


def test_real_variable_array_log_uniform():
    variable_array = RealVariableListLogUniform(bounds=(0.1, 10), nbins=5, length=3)
    assert variable_array.len == 3
    assert variable_array.num_amplify_variables == 12
    assert variable_array.encode([0.1, 0.3162278, 1.0]) == [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0]
    assert variable_array.decode([1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1]) == [1.0, 3.1622777, 10.0]
    assert isinstance(variable_array, VariableListBase)
    assert isinstance(variable_array[0], RealVariableLogUniform)


def test_discrete_variable_array():
    variable_array = DiscreteVariableList(discretized_list=[-1.0, 0.0, 0.5, 2.0], length=3)
    assert variable_array.len == 3
    assert variable_array.num_amplify_variables == 9
    assert variable_array.encode([-1.0, 2.0, 0.5]) == [0, 0, 0, 1, 1, 1, 1, 1, 0]
    assert variable_array.decode([1, 0, 0, 1, 1, 1, 1, 0, 0]) == [0.0, 2.0, 0.0]
    assert isinstance(variable_array, VariableListBase)
    assert isinstance(variable_array[0], DiscreteVariable)
    with pytest.raises(ValueError) as _:
        _ = variable_array.encode([0.0, 0.1, 0.5])
    variable_array = DiscreteVariableList(discretized_list=[-1.0, 0.0, 0.5, 2.0], length=3, method="one_hot")
    assert variable_array.num_amplify_variables == 12


def test_integer_variable_array():
    variable_array = IntegerVariableList(bounds=(0, 4), length=3)
    assert variable_array.len == 3
    assert variable_array.num_amplify_variables == 12
    assert variable_array.encode([0, 1, 2]) == [0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0]
    assert variable_array.decode([1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0]) == [1, 2, 3]
    assert isinstance(variable_array, VariableListBase)
    assert isinstance(variable_array[0], IntegerVariable)
    rng = np.random.default_rng(seed=1)
    random_value = variable_array.generate_random_value(rng)
    assert random_value == [2, 2, 3]

    random_value = variable_array.generate_random_value(rng, [2, 2, 3])
    assert random_value == [2, 2, 0]


def test_binary_variable_array():
    variable_array = BinaryVariableList(length=3)
    assert variable_array.len == 3
    assert variable_array.encode([False, True, False]) == [0, 1, 0]
    assert variable_array.decode([0, 1, 0]) == [False, True, False]
    assert variable_array[0].type is bool
    assert isinstance(variable_array, VariableListBase)
    assert isinstance(variable_array[0], BinaryVariable)
    rng = np.random.default_rng(seed=0)
    random_value = variable_array.generate_random_value(rng, [False, True, False])
    assert random_value == [False, True, True]


def test_discretized_list_amplify_encoder():
    discretized_list = [1, 2, 3, 4]
    with pytest.raises(ValueError) as _:
        _ = DiscreteVariable(discretized_list, method="amplify")


def test_discretized_list():
    discretized_list = [1, 2, 3, 4]
    variables = DiscreteVariable(discretized_list)
    assert variables.nbins == len(discretized_list)
    assert variables.num_amplify_variables == len(discretized_list) - 1
    assert variables.type is int
    assert variables.encode(3) == [1, 1, 0]
    assert variables.decode([1, 1, 1]) == 4
    with pytest.raises(ValueError) as _:  # 3.4 is not found in the discretized_list
        _ = variables.encode(3.4)


def test_real_variable_log_uniform_amplify_encoder():
    with pytest.raises(ValueError) as _:
        _ = RealVariableLogUniform((0.1, 10), 10, method="amplify")


def test_real_variable_log_uniform():
    variable = RealVariableLogUniform((0.1, 10), 10)
    assert variable.type is float
    assert variable.nbins == 10
    assert variable.num_amplify_variables == 9
    assert variable.encode(0.1) == [0] * 9
    assert variable.encode(5.99) == [1, 1, 1, 1, 1, 1, 1, 1, 0]
    assert variable.decode([1, 1, 1, 1, 1, 1, 1, 1, 0]) == 5.9948425
    assert variable.encode(3.80) == [1, 1, 1, 1, 1, 1, 1, 0, 0]

    variable = RealVariableLogUniform((0.1, 10), 10, method="one_hot")
    assert variable.nbins == 10
    assert variable.num_amplify_variables == 10
    assert variable.encode(0.1) == [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    assert variable.encode(5.99) == [0, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    assert variable.decode([0, 0, 0, 0, 0, 0, 0, 0, 1, 0]) == 5.9948425
    assert variable.encode(3.80) == [0, 0, 0, 0, 0, 0, 0, 1, 0, 0]
    with pytest.raises(ValueError) as _:
        _ = variable.encode(11.0)  # value > max
    with pytest.raises(ValueError) as _:
        _ = variable.encode(-0.1)  # value < min
    with pytest.raises(ValueError) as _:
        _ = RealVariableLogUniform((1, 5.0), 1)  # nbins = 1
    with pytest.raises(ValueError) as _:
        _ = RealVariableLogUniform((0.0, 5.0), 10, method="one_hot")  # min <= 0

    variable = RealVariableLogUniform((0.1, 10), 3)
    assert variable.encode(0.1) == [0, 0]
    assert variable.encode(1) == [1, 0]
    assert variable.encode(10) == [1, 1]
    discretized_list = [0.1, 1, 10]
    assert variable.discretized_list == discretized_list
    assert variable.idx_to_value(1) == discretized_list[1]
    incremental_array = (np.roll(discretized_list, -1) - np.array(discretized_list))[:2]
    generator = amplify.VariableGenerator()

    variable.issue_amplify_variable(generator, var_counter, var_name)
    q = variable.poly_array
    assert variable.to_amplify_poly() == (q * incremental_array).sum() + 0.1


def test_real_variable_amplify_encoder():
    with pytest.raises(ValueError) as _:
        _ = RealVariable((0.0, 5.0), 6, method="amplify")


def test_real_variable():
    variable = RealVariable((0.0, 5.0), 6)  # the defalt method is domain-wall
    assert variable.type is float
    assert variable.num_amplify_variables == 5
    assert variable.encode(1.0) == [1, 0, 0, 0, 0]
    assert variable.encode(1.1) == [1, 0, 0, 0, 0]
    assert variable.encode(1.5) == [1, 1, 0, 0, 0]
    assert variable.decode([1, 1, 0, 0, 0]) == 2.0
    generator = amplify.VariableGenerator()
    variable.issue_amplify_variable(generator, var_counter, var_name)
    q = variable.poly_array
    assert q is not None
    idx = q.sum()
    assert variable.to_amplify_poly() == idx

    rng = np.random.default_rng(seed=0)
    random_value = variable.generate_random_value(rng)
    assert random_value
    assert random_value == 5.0

    variable = RealVariable((0.0, 5.0), 4)  # the defalt method is domain-wall
    assert variable.num_amplify_variables == 3
    assert variable.delta == 5.0 / 3
    assert variable.encode(1.0) == [1, 0, 0]
    assert variable.encode(1.1) == [1, 0, 0]
    assert variable.encode(1 + variable.delta) == [1, 1, 0]
    assert variable.decode([1, 1, 0]) == 2 * variable.delta

    variable = RealVariable((0.0, 5.0), 4, method="one_hot")
    assert variable.num_amplify_variables == 4
    assert variable.encode(0.0) == [1, 0, 0, 0]
    assert variable.delta == 5.0 / 3
    mid_value = 2 * variable.delta + variable.bounds[0]
    assert variable.encode(mid_value) == [0, 0, 1, 0]
    assert variable.encode(5.0) == [0, 0, 0, 1]
    assert variable.decode([1, 0, 0, 0]) == 0.0
    assert variable.decode([0, 0, 1, 0]) == mid_value
    assert variable.decode([0, 0, 0, 1]) == 5.0
    with pytest.raises(ValueError) as _:
        _ = variable.encode(5.1)  # value > max
    with pytest.raises(ValueError) as _:
        _ = variable.encode(-0.1)  # value < min
    with pytest.raises(ValueError) as _:
        _ = RealVariable((0.0, 5.0), 1, method="one_hot")  # nbins = 1


def test_integer_variable_amplify_encoder():
    variable = IntegerVariable((0, 5), method="amplify")
    assert variable.bounds == (0, 5)
    assert variable.nbins == 1
    assert variable.num_amplify_variables == 1
    assert variable.type is int
    assert variable.encode(1) == [1]
    assert variable.encode(2) == [2]
    assert variable.encode(5) == [5]
    assert variable.decode([5]) == 5
    assert variable.decode([4]) == 4
    generator = amplify.VariableGenerator()
    with pytest.raises(RuntimeError) as _:
        _ = variable.binary_to_idx([0])
    with pytest.raises(RuntimeError) as _:
        _ = variable.idx_to_binary(0)
    with pytest.raises(RuntimeError) as _:
        _ = variable.value_to_idx(5)
    with pytest.raises(RuntimeError) as _:
        _ = variable.idx_to_value(5)

    variable.issue_amplify_variable(generator, var_counter, var_name)
    poly_array = variable.poly_array
    assert poly_array is not None
    assert len(poly_array) == variable.num_amplify_variables
    assert poly_array[0].as_variable().type == amplify.VariableType.Integer

    assert amplify.ConstraintList() == variable.generate_amplify_constraint()
    assert variable.to_amplify_poly() == poly_array
    rng = np.random.default_rng(seed=0)
    random_value = variable.generate_random_value(rng)
    assert random_value == 3


def test_integer_variable():
    variable = IntegerVariable((0, 5))  # the default method is domain-wall
    assert variable.bounds == (0, 5)
    assert variable.nbins == 6
    assert variable.num_amplify_variables == 5
    assert variable.type is int
    assert variable.encode(1) == [1, 0, 0, 0, 0]
    assert variable.encode(2) == [1, 1, 0, 0, 0]
    assert variable.encode(5) == [1, 1, 1, 1, 1]
    assert variable.decode([1, 1, 1, 1, 1]) == 5
    assert variable.decode([1, 1, 1, 1, 0]) == 4
    assert variable.decode([1, 0, 1, 1, 1]) == 4  # this is invalid from FMQA side, but OK as a unary variable
    generator = amplify.VariableGenerator()
    variable.issue_amplify_variable(generator, var_counter, var_name)
    poly_array = variable.poly_array
    assert poly_array is not None
    assert len(poly_array) == variable.num_amplify_variables
    assert poly_array[0].as_variable().type == amplify.VariableType.Binary

    idx = poly_array.sum()
    assert variable.to_amplify_poly() == idx
    rng = np.random.default_rng(seed=0)
    random_value = variable.generate_random_value(rng)
    assert random_value == 5

    variable = IntegerVariable((1, 5))  # the default method is domain-wall
    assert variable.encode(1) == [0, 0, 0, 0]
    assert variable.encode(2) == [1, 0, 0, 0]
    assert variable.encode(5) == [1, 1, 1, 1]
    assert variable.decode([1, 1, 1, 1]) == 5
    assert variable.decode([1, 1, 1, 0]) == 4
    assert variable.decode([0, 1, 1, 1]) == 4  # this is invalid from FMQA side, but OK as a domain-wall variable
    generator = amplify.VariableGenerator()
    variable.issue_amplify_variable(generator, var_counter, var_name)
    q1 = variable.poly_array
    assert q1 is not None
    idx = q1.sum()
    assert variable.to_amplify_poly() == idx + 1

    variable = IntegerVariable((0, 5), method="one_hot")
    assert variable.bounds == (0, 5)
    assert variable.nbins == 6
    assert variable.num_amplify_variables == 6
    assert variable.type is int
    assert variable.encode(0) == [1, 0, 0, 0, 0, 0]
    assert variable.encode(4) == [0, 0, 0, 0, 1, 0]
    assert variable.encode(5) == [0, 0, 0, 0, 0, 1]
    assert variable.decode([1, 0, 0, 0, 0, 0]) == 0
    assert variable.decode([0, 0, 0, 0, 1, 0]) == 4
    assert variable.decode([0, 0, 0, 0, 0, 1]) == 5
    generator = amplify.VariableGenerator()
    variable.issue_amplify_variable(generator, var_counter, var_name)
    q2 = variable.poly_array
    assert q2 is not None
    idx = (np.array(q2) * np.array(range(len(q2)), dtype=int)).sum()
    assert variable.to_amplify_poly() == idx
    with pytest.raises(ValueError) as _:
        _ = variable.encode(6)  # value > max
    with pytest.raises(ValueError) as _:
        _ = variable.encode(-1)  # value < min


def test_binary_variable():
    variable = BinaryVariable()
    assert variable.bounds == (False, True)
    assert variable.nbins == 1
    assert variable.delta == 0
    assert variable.type is bool
    assert variable.num_amplify_variables == 1

    assert variable.value_to_idx(False) == 0
    assert variable.value_to_idx(True) == 1
    assert variable.idx_to_value(1)
    assert not variable.idx_to_value(0)

    generator = amplify.VariableGenerator()
    variable.issue_amplify_variable(generator, var_counter, var_name)
    poly_array = variable.poly_array
    assert poly_array is not None
    assert len(poly_array) == variable.num_amplify_variables
    assert poly_array[0].as_variable().type == amplify.VariableType.Binary

    assert variable.to_amplify_poly() == poly_array[0]

    assert variable.binary_to_idx([0]) == 0
    assert variable.idx_to_binary(1) == [1]

    assert variable.encode(1) == [1]
    assert variable.decode([0]) == 0

    rng = np.random.default_rng(seed=1)
    assert variable.generate_random_value(rng) == 0
    assert variable.generate_random_value(rng) == 1
