# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

import io
import sys
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    import logging


def exec_func_neat_stdout(
    header: str,
    my_func: Callable,
    logger: logging.Logger | None = None,
    **kwargs: dict[str, Any],
) -> float:
    """Wrap the objective function to modify its standard output.

    Args:
        header (str): A string to add in front of the standard output from an objective function, `my_func`.
        my_func (Callable): An objective function to execute.
        logger (logging.Logger | None, optional): A logger. Defaults to `None`.
        **kwargs (dict[str, Any]): Additional keyword arguments to pass to `my_func`.

    Returns:
        float: Return value from the objective function.
    """
    # Store the original stdout
    original_stdout = sys.stdout

    # Create a temporary buffer for stdout
    stdout_buffer = io.StringIO()
    sys.stdout = stdout_buffer

    # Call the function
    ret = my_func(**kwargs)

    # Restore the original stdout
    sys.stdout = original_stdout

    # Print the captured output with additional indentation
    if stdout_buffer.getvalue():
        stdout = header + stdout_buffer.getvalue().replace("\n", "\n" + header).removesuffix("\n" + header)
        if logger is None:
            print(stdout)
        else:
            for string in stdout.split("\n"):
                logger.info(string)
    return ret


def print_to_str(*args, **kwargs) -> str:  # noqa: ANN002, ANN003
    """Call like `print()` but return a corresponding string.

    Returns:
        str: The string.
    """
    output = io.StringIO()
    print(*args, file=output, **kwargs)
    contents = output.getvalue()
    output.close()
    return contents.replace("\n\n", "\n")


short_line = "--------------------"
long_line = "----------------------------------------"
double_line = "========================================"
header_obj = "- [obj]: "
header_cycle = "- "
header_cycle = "- "
