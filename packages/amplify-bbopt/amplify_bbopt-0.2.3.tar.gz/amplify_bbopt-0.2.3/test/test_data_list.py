# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import pytest
from amplify_bbopt import DataList, FlatSolution, IntegerVariable, IntegerVariableList, Variables, load_dataset


def test_data_list():
    variables = Variables(
        a=IntegerVariable((0, 5)),
        b=IntegerVariableList((0, 5), 2),
    )

    x_in = [[0, 0, 0], [1, 1, 1], [1, 2, 3]]
    y_in = [0, 1, -2]
    names = ["a", "b[0]", "b[1]"]
    data = DataList(x=x_in, y=y_in, variable_names=names)  # type: ignore

    for i in range(len(data)):
        assert data[i] == (x_in[i], y_in[i])
        assert data.to_solution_dict(i) == {names[j]: x_in[i][j] for j in range(len(names))}

    structured = FlatSolution(variables, [0, 0, 0]).to_structured()
    assert data.to_structured_solution(variables, 0).values == structured.values
    assert data.to_structured_solution(variables, 0).names == structured.names

    for i, x in enumerate(data.to_structured_solution_list(variables)):
        assert x.to_flat().values == data.x[i]
        assert x.to_flat().names == data.variable_names
        assert x.values == data.to_structured_solution(variables, i).values
        assert x.names == data.to_structured_solution(variables, i).names

    assert data.abs_y_max == 2

    with pytest.raises(ValueError) as _:
        data = DataList()

    x_p, y_p = data.values
    assert x_in == x_p
    assert y_in == y_p

    assert data._filepath is None  # noqa: SLF001
    data.set_output_path("./test.csv")
    assert data._filepath == "./test.csv"  # noqa: SLF001

    x_in = [[0, 0, 0], [1, 1, 1]]
    y_in = [0, 1, -2]
    with pytest.raises(ValueError) as _:
        data = DataList(x=x_in, y=y_in)  # type: ignore

    x_in = [[0, 0, 0], [1, 1, 1], [1, 2, 3]]
    y_in = [0, 1, -2]
    data = DataList(x=x_in, y=y_in)  # type: ignore
    assert data.variable_names == ["x0", "x1", "x2"]


def test_load():
    filepath = "./test/data/test.csv"
    data = DataList(
        x=[[0, 0, 0], [1, 1, 1], [1, 2, 3]],
        y=[0, 1, -2],
        variable_names=["a", "b[0]", "b[1]"],
        filepath=filepath,
    )
    data.save()

    data_loaded = load_dataset(filepath)
    assert data_loaded._filepath == filepath  # noqa: SLF001
    assert ((data_loaded.to_df() == data.to_df()).all()).all()

    data_loaded = load_dataset(filepath, allow_overwrite=False)
    assert data_loaded._filepath is None  # noqa: SLF001
