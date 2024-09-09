# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from amplify_bbopt.solution_type import FlatSolution, FlatSolutionDict, StructuredSolution, StructuredSolutionDict
from amplify_bbopt.variable import IntegerVariable, IntegerVariableList
from amplify_bbopt.variables import Variables


def test_flattened_structured_dict():
    variables = Variables(
        a=IntegerVariable((0, 10)),
        b=IntegerVariableList((0, 10), 3),
        c=IntegerVariable((0, 10)),
    )

    structured_dict = StructuredSolutionDict({"a": 1, "b": [2, 3, 4], "c": 5})
    flat_dict = FlatSolutionDict({"a": 1, "b[0]": 2, "b[1]": 3, "b[2]": 4, "c": 5})

    assert structured_dict.to_solution(variables).values == StructuredSolution(variables, [1, [2, 3, 4], 5]).values
    assert flat_dict.to_solution(variables).values == FlatSolution(variables, [1, 2, 3, 4, 5]).values
    assert structured_dict.to_list() == StructuredSolution(variables, [1, [2, 3, 4], 5]).values
    assert flat_dict.to_list() == FlatSolution(variables, [1, 2, 3, 4, 5]).values


def test_flattened_structured():
    variables = Variables(
        a=IntegerVariable((0, 10)),
        b=IntegerVariableList((0, 10), 3),
        c=IntegerVariable((0, 10)),
    )
    structured = StructuredSolution(variables)
    structured = structured.from_solution_dict({"a": 1, "b": [2, 3, 4], "c": 5})
    assert structured.values == [1, [2, 3, 4], 5]
    assert structured.names == ["a", "b", "c"]
    assert structured.to_solution_dict() == {"a": 1, "b": [2, 3, 4], "c": 5}
    flat = FlatSolution(variables).from_solution_dict({"a": 1, "b[0]": 2, "b[1]": 3, "b[2]": 4, "c": 5})
    assert flat.values == [1, 2, 3, 4, 5]
    assert flat.names == ["a", "b[0]", "b[1]", "b[2]", "c"]
    assert flat.to_solution_dict() == {"a": 1, "b[0]": 2, "b[1]": 3, "b[2]": 4, "c": 5}
    assert flat.values == structured.to_flat().values
    assert structured.values == flat.to_structured().values

    assert structured[1] == ("b", [2, 3, 4])
    for i, item in enumerate(structured):
        assert structured.names[i], structured.values[i] == item

    assert flat[1] == ("b[0]", 2)
    for i, item in enumerate(flat):
        assert flat.names[i], flat.values[i] == item

    # copy test
    structured = StructuredSolution(variables).from_solution_dict({"a": 1, "b": [2, 3, 4], "c": 5})
    structured_ref = structured
    structured_ref.from_solution_dict({"a": 1, "b": [2, 3, 0], "c": 0})

    assert structured.values == structured_ref.values

    structured = StructuredSolution(variables).from_solution_dict({"a": 1, "b": [2, 3, 4], "c": 5})
    structured_ref = structured.copy()
    structured_ref.from_solution_dict({"a": 1, "b": [2, 3, 0], "c": 0})

    assert structured.values != structured_ref.values
