# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import Any

import amplify
import numpy as np
import pytest
from amplify_bbopt.solution_type import StructuredSolution
from amplify_bbopt.variable import (
    BinaryVariable,
    BinaryVariableList,
    IntegerVariable,
    IntegerVariableList,
    RealVariable,
    RealVariableLogUniform,
)
from amplify_bbopt.variables import Variables


def test_generate_random_value():
    variables = Variables(
        a0=BinaryVariable(),
        a1=IntegerVariable((0, 9)),
        a2=IntegerVariableList((0, 9), 2),
    )
    rng = np.random.default_rng(seed=0)

    original_sol = StructuredSolution(variables, [False, 0, [0, 0]])
    num_tests = 10
    # no find_neighbour = False
    average_dist = 0.0  # distance between original and new solutions
    for _ in range(num_tests):
        sol = variables.generate_random_value(rng, original_sol)
        average_dist += np.sqrt(((np.array(original_sol.to_flat().values) - np.array(sol.to_flat().values)) ** 2).sum())
    average_dist /= num_tests
    assert average_dist > 1

    # with find_neighbour = True
    average_dist = 0.0  # distance between original and new solutions
    for _ in range(num_tests):
        sol = variables.generate_random_value(rng, original_sol, True)
        average_dist += np.sqrt(((np.array(original_sol.to_flat().values) - np.array(sol.to_flat().values)) ** 2).sum())
    average_dist /= num_tests
    assert average_dist == 1


def test_convert_to_amplify_solution_dict():
    variables = Variables(
        a0=BinaryVariable(),
        a1=IntegerVariable((0, 2)),
        a2=IntegerVariableList((0, 2), 2),
    )
    # This assertion is to set all Amplify SDK variables.
    assert variables.poly_array is not None

    solution = StructuredSolution(variables, [False, 1, [0, 2]])
    amplify_sol_dict = variables.convert_to_amplify_solution_dict(solution.to_solution_dict())

    ans = dict(zip(variables.poly_array, [0, 1, 0, 0, 0, 1, 1]))
    assert list(amplify_sol_dict.keys()) == list(ans.keys())
    assert list(amplify_sol_dict.values()) == list(ans.values())


def test_unify_variables():
    variables_a = Variables(
        a0=BinaryVariable(),
        a1=IntegerVariable((0, 5)),
        a2=IntegerVariableList((0, 5), 2),
    )

    variables_b = Variables(
        b0=BinaryVariable(),
        b1=IntegerVariable((0, 5)),
        a2=IntegerVariableList((0, 5), 2),
    )

    variable_dict_universe: dict[str, Any] = {}
    variable_dict_universe.update(variables_a.var_dict)
    variable_dict_universe.update(variables_b.var_dict)

    assert variables_a.names == ["a0", "a1", "a2"]
    assert variables_b.names == ["b0", "b1", "a2"]


def test_variables_integer_amplify_encoding():
    variables = Variables(
        a=IntegerVariable((0, 5), method="amplify"),
        b=IntegerVariableList((0, 5), 2, method="amplify"),
    )
    assert variables.num_amplify_variables == 3
    assert variables.encode(StructuredSolution(variables, [2, [1, 0]])) == [2, 1, 0]
    assert variables.decode([2, 1, 0]).values == StructuredSolution(variables, [2, [1, 0]]).values
    variables.issue_amplify_variable()
    q = variables.poly_array
    gen = amplify.VariableGenerator()
    q_ans = gen.array("Integer", bounds=(0, 5), shape=3)
    for i in range(len(q)):
        assert str(q[i].as_variable().type) == str(q_ans[i].as_variable().type)

    variables = Variables(
        a=IntegerVariable((0, 5), method="amplify"),
        b=RealVariable((0, 5), 10),  # domain-wall
        c=IntegerVariableList((0, 5), 2, method="amplify"),
        d=BinaryVariable(),
    )
    assert variables.num_amplify_variables == 13
    assert variables.encode(StructuredSolution(variables, [2, 0.0, [1, 0], True])) == [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]  # fmt: skip # noqa: E501
    assert (
        variables.decode([2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1]).values
        == StructuredSolution(variables, [2, 0.0, [1, 0], True]).values
    )
    variables.issue_amplify_variable()
    q = variables.poly_array
    gen = amplify.VariableGenerator()
    n0 = gen.scalar("Integer", bounds=(0, 5))
    q0 = [gen.scalar("Binary") for _ in range(9)]
    n1 = gen.scalar("Integer", bounds=(0, 5))
    n2 = gen.scalar("Integer", bounds=(0, 5))
    q1 = gen.scalar("Binary")
    q_ans = amplify.PolyArray([n0, *q0, n1, n2, q1])
    for i in range(len(q)):
        assert str(q[i].as_variable().type) == str(q_ans[i].as_variable().type)


def test_variables_variable_array():
    variables = Variables(a=BinaryVariable(), b=BinaryVariableList(3), c=BinaryVariable())
    assert variables.num_amplify_variables == 5
    assert variables.encode(StructuredSolution(variables, [True, [True, True, True], True])) == [1, 1, 1, 1, 1]
    assert (
        variables.decode([1, 1, 1, 1, 1]).values
        == StructuredSolution(variables, [True, [True, True, True], True]).values
    )


def test_too_many_encoder_decoder_one_hot():
    variables = Variables(
        q0=IntegerVariable((0, 5), method="one_hot"),
        q1=IntegerVariable((0, 5), method="one_hot"),
    )
    integers = [1, 3, 5]
    binary = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0]
    with pytest.raises(RuntimeError) as _:
        _ = variables.encode(StructuredSolution(variables, integers))  # type: ignore
    with pytest.raises(RuntimeError) as _:
        _ = variables.decode(binary)  # type: ignore


def test_mixed_encoder_decoder():
    variables = Variables(
        q0=BinaryVariable(),
        q1=IntegerVariable((0, 5)),  # 0, 1, 3, 4, 5
        q2=RealVariable((0.0, 1.0), 3),  # 0.0  0.5  1.0
        q3=RealVariableLogUniform((2, 8), 3),  # 2.0  4.0  8.0
    )
    values = [True, 3, 0.5, 4.0]
    binary = [1, 1, 1, 1, 0, 0, 1, 0, 1, 0]
    encoded = variables.encode(StructuredSolution(variables, values))  # type: ignore
    decoded = variables.decode(binary).values  # type: ignore
    assert encoded == binary
    assert decoded == values

    variables = Variables(
        q0=BinaryVariable(),
        q1=IntegerVariable((0, 5), method="one_hot"),
        q2=RealVariable((0.0, 1.0), 3, method="one_hot"),
        q3=RealVariableLogUniform((2, 8), 3, method="one_hot"),
    )
    values = [True, 3, 0.5, 4.0]
    binary = [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0]
    encoded = variables.encode(StructuredSolution(variables, values))  # type: ignore
    decoded = variables.decode(binary).values  # type: ignore
    assert encoded == binary
    assert decoded == values


def test_real_log_uniform_encoder_decoder():
    variables = Variables(
        q0=RealVariableLogUniform((0.1, 10.0), 3),
        q1=RealVariableLogUniform((2, 8), 3),
    )
    reals = [10.0, 4]
    binary = [1, 1, 1, 0]
    decoded_from_encoded = [10.0, 4.0]
    encoded = variables.encode(StructuredSolution(variables, reals))  # type: ignore
    decoded = variables.decode(binary).values  # type: ignore
    assert encoded == binary
    assert decoded == decoded_from_encoded

    variables = Variables(
        q0=RealVariableLogUniform((0.1, 10.0), 3, method="one_hot"),
        q1=RealVariableLogUniform((2, 8), 3, method="one_hot"),
    )
    reals = [10.0, 4]
    binary = [0, 0, 1, 0, 1, 0]
    decoded_from_encoded = [10.0, 4.0]
    encoded = variables.encode(StructuredSolution(variables, reals))  # type: ignore
    decoded = variables.decode(binary).values  # type: ignore
    assert encoded == binary
    assert decoded == decoded_from_encoded


def test_integer_encoder_decoder():
    variables = Variables(
        q0=IntegerVariable((0, 5)),
        q1=IntegerVariable((1, 5)),
        q2=IntegerVariable((-1, 4)),
    )
    integers = [1, 3, 4]
    binary = [1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1]
    encoded = variables.encode(StructuredSolution(variables, integers))  # type: ignore
    decoded = variables.decode(binary).values  # type: ignore
    assert encoded == binary
    assert decoded == integers

    variables = Variables(
        q0=IntegerVariable((0, 5), method="one_hot"),
        q1=IntegerVariable((1, 5), method="one_hot"),
        q2=IntegerVariable((-1, 4), method="one_hot"),
    )
    integers = [1, 3, 4]
    binary = [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1]
    encoded = variables.encode(StructuredSolution(variables, integers))  # type: ignore
    decoded = variables.decode(binary).values  # type: ignore
    assert encoded == binary
    assert decoded == integers


def test_binary_encoder_decoder():
    variables = Variables(q0=BinaryVariable(), q1=BinaryVariable(), q2=BinaryVariable())
    binary_list = [1, 0, 1]
    encoded = variables.encode(StructuredSolution(variables, binary_list))  # type: ignore
    decoded = variables.decode(binary_list).values  # type: ignore

    assert encoded == binary_list
    assert decoded == binary_list


def test_variables():
    binary_variable = BinaryVariable()
    integer_variable = IntegerVariable((0, 5))
    real_variable = RealVariable((0.0, 5.0), 5)
    real_variable_log_uniform = RealVariableLogUniform((0.1, 10.0), 3)
    variables = Variables(
        binary_variable=binary_variable,
        integer_variable=integer_variable,
        real_variable=real_variable,
        real_variable_log_uniform=real_variable_log_uniform,
    )
    assert len(variables) == 4
    assert variables.num_amplify_variables == 12
    assert variables.var_dict["binary_variable"] == binary_variable
    assert variables.var_dict["integer_variable"] == integer_variable
    assert variables.var_dict["real_variable"] == real_variable
    assert variables.var_dict["real_variable_log_uniform"] == real_variable_log_uniform

    num_variables = 10
    var_names = [f"q{i}" for i in range(num_variables)]
    dc = {key: BinaryVariable() for key in var_names}
    my_variables = Variables(**dc)
    assert len(my_variables) == num_variables
    assert my_variables.num_amplify_variables == num_variables
