# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

import copy
import pathlib
import sys
from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

from .logger import logger
from .solution_type import FlatSolution, FlatSolutionDict, StructuredSolution

if TYPE_CHECKING:
    from collections.abc import Iterator

    from .variables import Variables


class DataList:
    """A class to handle input-output pairs of a black-box function."""

    def __init__(
        self,
        x: list[list[bool | int | float]] | None = None,
        y: list[int | float] | None = None,
        variable_names: list[str] | None = None,
        filepath: str | None = None,
    ) -> None:
        """Initialize the data list class.

        Args:
            x (list[list[bool | int | float]] | None, optional): A list of the input vectors. Defaults to `None`.
            y (list[int | float] | None, optional): A list of the output values. Defaults to `None`.
            variable_names (list[str] | None, optional): A list of the variable names. Defaults to `None`.
            filepath (str | None, optional): A filepath to save the data with :func:`save` method. Defaults to `None`.

        Raises:
            ValueError: If only one of  (x, y) is specified.
            ValueError: If x and y do not have the same length.
            ValueError: If at least one of the data (x, y) or `variable_names` is not specified.
        """
        if x is None and y is None:
            self._x: list[list[bool | int | float]] = []
            self._y: list[int | float] = []
        elif x is not None and y is not None:
            if len(x) != len(y):
                raise ValueError("x and y must have the same number of samples.")
            self._x = x
            self._y = y  # type: ignore
        else:
            raise ValueError("either both (x, y) or none of (x, y) must be passed.")

        if not len(self._x) == len(self._y):
            raise ValueError("x and y must have the same length.")

        if variable_names is not None:
            self._variable_names = variable_names
        else:
            if x is None and y is None:
                raise ValueError("Either the data (x, y) or variable_names needs to be specified.")
            assert x is not None
            self._variable_names = (
                ["x" + str(i) for i in range(len(x[0]))] if variable_names is None else variable_names
            )

        self._filepath = filepath

    @property
    def variable_names(self) -> list[str] | None:
        """Names of the variables."""
        return self._variable_names

    def append(
        self,
        value: tuple[list[bool | int | float], int | float],
    ) -> None:
        """Append an input-output pair.

        Args:
            value (tuple[list[bool | int | float], int | float]): A tuple of input and output.
        """
        self._x.append(value[0])
        self._y.append(value[1])

    def __len__(self) -> int:
        """Length of the data list.

        Returns:
            int: The length.
        """
        return len(self._y)

    def __getitem__(self, i: int) -> tuple[list[bool | int | float], int | float]:
        """Return a tuple of the input vector and output value.

        Args:
            i (int): Index.

        Returns:
            tuple[list[bool | int | float], int | float]: A tuple of the input vector and output value.
        """
        return self._x[i], self._y[i]

    def __iter__(self) -> Iterator[tuple]:
        """A tuple of the input vector and output value.

        Yields:
            tuple[list[bool | int | float], int | float]: A tuple of the input vector and output value.
        """
        yield from zip(self._x, self._y)

    def to_df(self) -> pd.DataFrame:
        """Convert and return the data to :obj:`pandas.DataFrame`.

        Returns:
            pandas.DataFrame: The converted data.
        """
        index = ["Sample #" + str(i) for i in range(len(self))]
        df = pd.DataFrame(self._x, index=index, columns=self._variable_names)
        df["black-box objective"] = self._y
        return df

    def to_solution_dict(self, i: int) -> FlatSolutionDict:
        """Convert to the solution dict. This can be used for multi-objective optimization where there is no one specific :obj:`Variables` assigned for the multiple objectives.

        Args:
            i (int): Index of the sample.

        Returns:
            FlatSolutionDict: The resulting solution dict.
        """  # noqa: E501
        return FlatSolutionDict(dict(zip(self._variable_names, self._x[i])))

    def to_structured_solution(self, variables: Variables, i: int) -> StructuredSolution:
        """Convert the i-th data (input) to :obj:`StructuredSolution`.

        Args:
            variables (Variables): A :obj:`Variables` instance that is relevant to the black-box objective function class that this :obj:`DataList` is for.
            i (int): Index of the sample.

        Returns:
            StructuredSolution: A converted input vector.
        """  # noqa: E501
        return FlatSolution(variables, self._x[i]).to_structured()

    def to_structured_solution_list(self, variables: Variables) -> list[StructuredSolution]:
        """Convert the data (all input vectors) to a list of :obj:`StructuredSolution`.

        Args:
            variables (Variables): A :obj:`Variables` instance that is relevant to the black-box objective function class that this :obj:`DataList` is for.

        Returns:
            list[StructuredSolution]: A list of converted input vectors.
        """  # noqa: E501
        return [FlatSolution(variables, self._x[j]).to_structured() for j in range(len(self))]

    def save(self) -> None:
        """Save the data if the filepath is set either in the :obj:`DataList.__init__` or with the :obj:`DataList.set_output_path` method."""  # noqa: E501
        if self._filepath is not None:
            self.to_df().to_csv(pathlib.Path(self._filepath).resolve())
            logger().info(f"data saved as {self._filepath}")

    def set_output_path(self, filepath: str | None) -> None:
        """Set a output file path.

        Args:
            filepath (str | None): A file path.
        """
        self._filepath = filepath

    def is_unique(self, solution_dict: FlatSolutionDict) -> bool:
        if len(self._x) == 0:
            return True
        return not np.array([x == list(solution_dict.values()) for x in self._x]).max()

    @property
    def values(self) -> tuple[list[list[bool | int | float]], list[int | float]]:
        """Return input vectors and output values.

        Returns:
            tuple[list[list[bool | int | float]], list[int | float]]: A tuple of the lists of the input vectors and the corresponding output values.
        """  # noqa: E501
        return self._x, self._y

    @property
    def abs_y_max(self) -> float:
        """The absolute maximum value in the output values in the current dataset."""
        return np.abs(np.array(self._y)[self._y is not None]).max()

    @property
    def x(self) -> list[list[bool | int | float]]:
        """The list of the input vectors."""
        return self._x

    @property
    def y(self) -> list[int | float]:
        """The list of the output values. `None` elements are replaced with `0.5 * sys.float_info.max`."""
        return np.nan_to_num(
            np.array(self._y, dtype=float), copy=True, nan=0.5 * sys.float_info.max
        ).tolist()  # requires "dtype=float" when the list contains both numbers and None.

    def copy(self) -> DataList:
        """Deepcopy an instantce of the class.

        Returns:
            DataList: The copied data.
        """
        return DataList(
            copy.deepcopy(self._x),
            copy.deepcopy(self._y),
            variable_names=copy.deepcopy(self._variable_names),
            filepath=self._filepath,
        )


def load_dataset(filepath: str, allow_overwrite: bool = True) -> DataList:
    """Load the :obj:`DataList` data in csv. The data consists of all the input values to a black-box objective function in a respective order, and the last column contains the corresponding output from the black-box function.

    Args:
        filepath (str): A data filepath.
        allow_overwrite (bool, optional): If set True, the filepath will be set in the returned :obj:`DataList` class instance so that when its :obj:`DataList.save` method is called later, the file will be overwritten. In Amplify-BBOpt, :obj:`DataList.save` is called at end of each optimization cycle. Defaults to `True` (to be overwritten).

    Returns:
        DataList: The loaded data list.
    """  # noqa: E501
    df = pd.read_csv(pathlib.Path(filepath).resolve(), index_col=0)
    y_column_name = df.columns[-1]  # the last column
    y = df[y_column_name].values.tolist()
    x = df.drop(columns=y_column_name).values.tolist()
    names = df.drop(columns=y_column_name).columns.to_list()
    logger().info(f"data loaded from {filepath}")
    if allow_overwrite:
        return DataList(x, y, variable_names=names, filepath=filepath)
    return DataList(x, y, names)
    return DataList(x, y, names)
    return DataList(x, y, names)
