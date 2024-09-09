# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from typing import Annotated

import numpy as np
from amplify_bbopt import BinaryVariableList, DataList, DatasetGenerator, blackbox, equal_to


@blackbox
def objective_func(
    x: Annotated[list[bool], BinaryVariableList(length=10)],
):
    return sum(x)


def test_generate_init_data():
    variables = objective_func.variables
    rhs_value = 5
    # sum of variables.x is considered implicitly
    assert isinstance(variables.x, BinaryVariableList)
    c = equal_to(variables.x, rhs_value)
    objective_func.add_constraint(c)
    gen = DatasetGenerator(objective=objective_func)
    data = gen.generate(num_samples=2)
    assert isinstance(data, DataList)
    assert np.array(data.x[0]).sum() == rhs_value
    assert np.array(data.x[1]).sum() == rhs_value
