# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from amplify_bbopt.variable import IntegerVariable, RealVariableList


def test_poly():
    variable = IntegerVariable((0, 3))
    variable_array = RealVariableList(bounds=(-1, 0), nbins=3, length=2)
    poly0 = variable + variable_array[0]
    assert poly0.terms == {variable: 1.0, variable_array[0]: 1.0}
    poly1 = variable - variable_array[0]
    assert poly1.terms == {variable: 1.0, variable_array[0]: -1.0}
    poly2 = variable * 2.0 - 3.0 * variable_array[0]
    assert poly2.terms == {variable: 2.0, variable_array[0]: -3.0}
    poly3 = variable + variable_array
    assert poly3.terms == {variable: 1.0, variable_array[0]: 1.0, variable_array[1]: 1.0}
    poly4 = variable + 2.0 * variable_array
    assert poly4.terms == {variable: 1.0, variable_array[0]: 2.0, variable_array[1]: 2.0}
    poly5 = variable - variable_array * 2.5
    assert poly5.terms == {variable: 1.0, variable_array[0]: -2.5, variable_array[1]: -2.5}
