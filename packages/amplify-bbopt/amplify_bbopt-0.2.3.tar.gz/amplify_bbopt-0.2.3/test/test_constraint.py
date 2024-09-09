# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import Any

import amplify
import pytest
from amplify_bbopt import (
    Constraints,
    DiscreteVariable,
    IntegerVariable,
    IntegerVariableList,
    Poly,
    RealVariableLogUniform,
    StructuredSolution,
    Variables,
    clamp,
    equal_to,
    greater_equal,
    less_equal,
)


def test_unify_variables():
    # =================================
    # When no duplicate variables exist
    # =================================

    variables_a = Variables(
        a0=IntegerVariable((0, 5)),
        a1=IntegerVariableList((0, 5), 2),
    )

    variables_b = Variables(
        b0=IntegerVariable((0, 5)),
        b1=IntegerVariableList((0, 5), 2),
    )

    c = equal_to(variables_b.b0 + variables_a.a0, 5)
    with pytest.raises(RuntimeError) as _:
        # amplify.PolyArray is not issued for variables yet.
        c.to_amplify_constraint()

    print(f"{c=}")
    variables_a.issue_amplify_variable()
    variables_b.issue_amplify_variable()
    with pytest.raises(ValueError) as _:
        # operation between PolyArrays with different variable generator.
        c.to_amplify_constraint()

    # Reset
    variables_a.nullify_poly_array()
    variables_b.nullify_poly_array()
    # Since each of objectives have no duplicate variable, no var_dict_universe is necessary
    gen = amplify.VariableGenerator()
    variables_a.unify_variables(variables_a.var_dict, gen)
    variables_b.unify_variables(variables_b.var_dict, gen)
    poly_array_a = variables_a.a0.poly_array
    poly_array_b = variables_b.b0.poly_array
    c0 = c.to_amplify_constraint()
    assert poly_array_a is not None
    assert poly_array_b is not None
    c1 = amplify.equal_to(poly_array_a + poly_array_b, 5)
    assert c0.penalty == c1.penalty
    # ==============================
    # When duplicate variables exist
    # ==============================

    variables_a = Variables(
        a0=IntegerVariable((0, 5)),
        a1=IntegerVariableList((0, 5), 2),
    )

    variables_b = Variables(
        a0=IntegerVariable((0, 5)),
        b1=IntegerVariableList((0, 5), 2),
    )

    assert isinstance(variables_b.b1, IntegerVariableList)
    c = equal_to(variables_a.a0 + variables_b.b1[0], 5)
    with pytest.raises(RuntimeError) as _:
        # amplify.PolyArray is not issued for variables yet.
        c.to_amplify_constraint()

    variables_a.issue_amplify_variable()
    variables_b.issue_amplify_variable()
    assert variables_a.a0.poly_array is not None
    assert variables_b.a0.poly_array is not None

    with pytest.raises(ValueError) as _:
        # arithmetic operation between polynomials with different variable allocator is invalid
        assert variables_a.a0.poly_array == variables_b.a0.poly_array

    # Reset
    variables_a.nullify_poly_array()
    variables_b.nullify_poly_array()
    # Since each of objectives have duplicate variable, var_dict_universe is NECESSARY!
    gen = amplify.VariableGenerator()
    variables_a.unify_variables(variables_a.var_dict, gen)
    variables_b.unify_variables(variables_b.var_dict, gen)

    assert variables_a.a0.poly_array is not None
    assert variables_b.a0.poly_array is not None
    assert not (variables_a.a0.poly_array == variables_b.a0.poly_array).all()

    # Reset
    variables_a.nullify_poly_array()
    variables_b.nullify_poly_array()
    # Let's prepare var_dict_universe to unify variables
    var_dict_universe: dict[str, Any] = {}
    gen = amplify.VariableGenerator()
    var_dict_universe.update(variables_a.var_dict)
    var_dict_universe.update(variables_b.var_dict)
    variables_a.unify_variables(var_dict_universe, gen)
    variables_b.unify_variables(var_dict_universe, gen)
    assert (variables_a.a0.poly_array == variables_b.a0.poly_array).all()

    c.unify_variables(var_dict_universe)
    poly_array_a = variables_a.a0.poly_array
    poly_array_b = variables_b.b1[0].poly_array
    c0 = c.to_amplify_constraint()
    assert poly_array_a is not None
    assert poly_array_b is not None
    c1 = amplify.equal_to(poly_array_a + poly_array_b, 5)
    assert c0.penalty == c1.penalty


def test_constraint_list():
    variables = Variables(int_var_0=IntegerVariable((-10, 10)), int_var_1=IntegerVariable((-10, 10)))
    c_list = Constraints()
    c_list.append(equal_to(variables.int_var_0 + variables.int_var_1, 5))
    c_list.append(equal_to(variables.int_var_0 - variables.int_var_1, 1))
    assert c_list.is_satisfied(StructuredSolution(variables, [3, 2]).to_flat().to_solution_dict())

    c_list = Constraints([
        equal_to(variables.int_var_0 + variables.int_var_1, 5),
        equal_to(variables.int_var_0 - variables.int_var_1, 1),
    ])
    assert c_list.is_satisfied(StructuredSolution(variables, [3, 2]).to_flat().to_solution_dict())

    c_list = Constraints()
    c_list.append([
        equal_to(variables.int_var_0 + variables.int_var_1, 5),
        equal_to(variables.int_var_0 - variables.int_var_1, 1),
    ])
    c_list2 = Constraints()
    c_list2.append(c_list)
    assert c_list2.is_satisfied(StructuredSolution(variables, [3, 2]).to_flat().to_solution_dict())

    c_list = Constraints()
    c_list.append(equal_to(variables.int_var_0 + variables.int_var_1, 5))
    assert variables.poly_array is not None
    amp_c0 = c_list.to_amplify_constraint()
    amp_c1 = amplify.equal_to(variables.int_var_0.to_amplify_poly() + variables.int_var_1.to_amplify_poly(), 5)
    assert amp_c0[0].penalty == amp_c1.penalty


def test_constraint_variable_array_getitem():
    num_variables = 2
    variables = Variables(vars=IntegerVariableList((-10, 10), num_variables))
    eq_temp = Poly()
    assert isinstance(variables.vars, IntegerVariableList)
    for i in range(num_variables):
        eq_temp += variables.vars[i]
    c_eq = equal_to(eq_temp, 5)
    print(f"{c_eq=}")

    assert c_eq.is_satisfied(StructuredSolution(variables, [[-1, 6]]).to_flat().to_solution_dict())
    assert not c_eq.is_satisfied(StructuredSolution(variables, [[-1, 10]]).to_flat().to_solution_dict())


def test_eq():
    variables = Variables(int_var_0=IntegerVariable((-10, 10)), int_var_1=IntegerVariable((-10, 10)))
    c_eq = equal_to(variables.int_var_0 + variables.int_var_1, 5)
    assert c_eq.is_satisfied(StructuredSolution(variables, [-1, 6]).to_flat().to_solution_dict())
    assert not c_eq.is_satisfied(StructuredSolution(variables, [-1, 10]).to_flat().to_solution_dict())

    c_eq = equal_to(2 * variables.int_var_0 + 3 * variables.int_var_1, 5)
    assert c_eq.is_satisfied(StructuredSolution(variables, [1, 1]).to_flat().to_solution_dict())
    assert not c_eq.is_satisfied(StructuredSolution(variables, [1, 10]).to_flat().to_solution_dict())

    c_eq = equal_to(2 * variables.int_var_0 - variables.int_var_1, 5)
    assert c_eq.is_satisfied(StructuredSolution(variables, [5, 5]).to_flat().to_solution_dict())
    assert not c_eq.is_satisfied(StructuredSolution(variables, [2, -2]).to_flat().to_solution_dict())

    c_eq.weight = 10
    assert c_eq.weight == 10

    c_eq.penalty_formulation = "Relaxation"
    assert c_eq.penalty_formulation == "Relaxation"


def test_eq_array():
    variables = Variables(int_vars=IntegerVariableList((-10, 10), 3))
    assert isinstance(variables.int_vars, IntegerVariableList)
    c_eq = equal_to(variables.int_vars.sum(), 3)
    assert c_eq.is_satisfied(StructuredSolution(variables, [[1, 1, 1]]).to_flat().to_solution_dict())
    assert not c_eq.is_satisfied(StructuredSolution(variables, [[1, 1, 2]]).to_flat().to_solution_dict())


def test_eq_array_implicit_sum():
    variables = Variables(int_vars=IntegerVariableList((-10, 10), 3))
    assert isinstance(variables.int_vars, IntegerVariableList)
    c_eq = equal_to(variables.int_vars, 3)
    assert c_eq.is_satisfied(StructuredSolution(variables, [[1, 1, 1]]).to_flat().to_solution_dict())
    assert not c_eq.is_satisfied(StructuredSolution(variables, [[1, 1, 2]]).to_flat().to_solution_dict())


def test_eq_real_variable_log_unform():
    variables = Variables(var_0=RealVariableLogUniform((0.1, 10), 10), var_1=RealVariableLogUniform((0.1, 100), 10))
    c_le = less_equal(2 * variables.var_0 + variables.var_1, 10.0)
    assert c_le.is_satisfied(StructuredSolution(variables, [1.0, 8.0]).to_flat().to_solution_dict())
    assert not c_le.is_satisfied(StructuredSolution(variables, [1.1, 8.0]).to_flat().to_solution_dict())


def test_eq_discrete_variable():
    variables = Variables(var_0=DiscreteVariable([1, 2, 3, 4]), var_1=DiscreteVariable([5, 6, 7, 8]))
    c_eq = equal_to(variables.var_0 + variables.var_1, 10)
    assert c_eq.is_satisfied(StructuredSolution(variables, [2, 8]).to_flat().to_solution_dict())
    assert not c_eq.is_satisfied(StructuredSolution(variables, [2, 7]).to_flat().to_solution_dict())


def test_le():
    variables = Variables(int_var_0=IntegerVariable((-10, 10)), int_var_1=IntegerVariable((-10, 10)))
    c_le = less_equal(variables.int_var_0 + variables.int_var_1, 5)
    assert c_le.is_satisfied(StructuredSolution(variables, [6, -1]).to_flat().to_solution_dict())
    assert not c_le.is_satisfied(StructuredSolution(variables, [10, 1]).to_flat().to_solution_dict())

    c_le = less_equal(2 * variables.int_var_0 + variables.int_var_1, 5)
    assert c_le.is_satisfied(StructuredSolution(variables, [2, 1]).to_flat().to_solution_dict())
    assert not c_le.is_satisfied(StructuredSolution(variables, [2, 2]).to_flat().to_solution_dict())


def test_ge():
    variables = Variables(int_var_0=IntegerVariable((-10, 10)), int_var_1=IntegerVariable((-10, 10)))
    c_ge = greater_equal(variables.int_var_1 - variables.int_var_0, 0)
    assert c_ge.is_satisfied(StructuredSolution(variables, [-1, 0]).to_flat().to_solution_dict())
    assert not c_ge.is_satisfied(StructuredSolution(variables, [2, 1]).to_flat().to_solution_dict())


def test_cl():
    variables = Variables(int_var_0=IntegerVariable((-10, 10)), int_var_1=IntegerVariable((-10, 10)))
    c_cl = clamp(variables.int_var_1 + variables.int_var_0, (0, 5))
    assert c_cl.is_satisfied(StructuredSolution(variables, [1, 2]).to_flat().to_solution_dict())
    assert not c_cl.is_satisfied(StructuredSolution(variables, [-1, 0]).to_flat().to_solution_dict())
    with pytest.raises(ValueError) as _:
        _ = clamp(variables.int_var_1 + variables.int_var_0, (5, 0))


def test_amplify_constraint():
    variables = Variables(int_var_0=IntegerVariable((-10, 10)), int_var_1=IntegerVariable((-10, 10), method="amplify"))
    variables.issue_amplify_variable()
    q = variables.poly_array

    c_eq = equal_to(variables.int_var_0 + variables.int_var_1, 5)
    c_eq_amp = c_eq.to_amplify_constraint()
    encoded = variables.encode(StructuredSolution(variables, [1, 4]))
    mapping: dict[amplify.Poly, float] = {q[i]: encoded[i] for i in range(variables.num_amplify_variables)}
    assert c_eq_amp.is_satisfied(mapping)

    encoded = variables.encode(StructuredSolution(variables, [2, 4]))
    mapping = {q[i]: encoded[i] for i in range(variables.num_amplify_variables)}
    assert not c_eq_amp.is_satisfied(mapping)

    c_le = less_equal(2.0 * variables.int_var_0 - variables.int_var_1, 5)
    c_le_amp = c_le.to_amplify_constraint()
    encoded = variables.encode(StructuredSolution(variables, [3, 1]))
    mapping = {q[i]: encoded[i] for i in range(variables.num_amplify_variables)}
    assert c_le_amp.is_satisfied(mapping)

    encoded = variables.encode(StructuredSolution(variables, [5, 1]))
    mapping = {q[i]: encoded[i] for i in range(variables.num_amplify_variables)}
    assert not c_le_amp.is_satisfied(mapping)

    c_ge = greater_equal(2.0 * variables.int_var_0 - variables.int_var_1, 5)
    c_ge_amp = c_ge.to_amplify_constraint()
    encoded = variables.encode(StructuredSolution(variables, [4, 3]))
    mapping = {q[i]: encoded[i] for i in range(variables.num_amplify_variables)}
    assert c_ge_amp.is_satisfied(mapping)

    encoded = variables.encode(StructuredSolution(variables, [3, 3]))
    mapping = {q[i]: encoded[i] for i in range(variables.num_amplify_variables)}
    assert not c_ge_amp.is_satisfied(mapping)

    c_cl = clamp(2.0 * variables.int_var_0 - variables.int_var_1, (3, 5))
    c_cl_amp = c_cl.to_amplify_constraint()
    encoded = variables.encode(StructuredSolution(variables, [2, 1]))
    mapping = {q[i]: encoded[i] for i in range(variables.num_amplify_variables)}
    assert c_cl_amp.is_satisfied(mapping)

    encoded = variables.encode(StructuredSolution(variables, [1, 1]))
    mapping = {q[i]: encoded[i] for i in range(variables.num_amplify_variables)}
    assert not c_cl_amp.is_satisfied(mapping)
