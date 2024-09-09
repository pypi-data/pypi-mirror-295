# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from amplify_bbopt import exec_func_neat_stdout, print_to_str


def test_exec_func_neat_stdout():
    def my_func(x: int) -> float:
        print(f"{x=}")
        return 2 * x

    y = exec_func_neat_stdout("- [obj]", my_func, x=10)  # type: ignore

    assert y == 20


def test_print_to_str(capsys):
    print("before test")
    string = print_to_str(f"test {1=}")
    assert string == "test 1=1\n"
    print("after test")
    captured = capsys.readouterr()
    assert captured.out == "before test\n" + "after test\n"
