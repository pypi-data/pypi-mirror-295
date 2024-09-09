# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from .data_list import DataList

# Column names for history
ELAPSED = "elapsed time (s)"
OBJ_BB = "objective (blackbox)"
OBJ_CST = "objective (custom)"
OBJ_TOT = "objective (total)"
DEDUP = "de duplication"


class History:
    def __init__(
        self,
        data_list: DataList,
        elapsed_time: list[float] | None = None,
        is_de_duplication: list[bool] | None = None,
        custom_objective: list[float] | None = None,
        num_initial_data: int | None = None,
    ) -> None:
        if elapsed_time is not None and len(data_list) != len(elapsed_time):
            raise ValueError(
                f"data_list and elapsed_time must have the same length. {len(data_list)=},  {len(elapsed_time)=}."
            )
        if is_de_duplication is not None and len(data_list) != len(is_de_duplication):
            raise ValueError(
                "data_list and is_de_duplication must have the same length. "
                f"{len(data_list)=}, {len(is_de_duplication)=}."
            )
        if custom_objective is not None and len(data_list) != len(custom_objective):
            raise ValueError(
                "data_list and custom_objective must have the same length. "
                f"{len(data_list)=}, {len(custom_objective)=}."
            )

        index = ["Sample #" + str(i) for i in range(len(data_list))]
        self._hist_df = pd.DataFrame(data_list.x, index=index, columns=data_list.variable_names)
        self._hist_df[OBJ_BB] = data_list.y
        if custom_objective is not None:
            self._hist_df[OBJ_CST] = custom_objective
        else:
            custom_objective = [0.0] * len(data_list)

        self._hist_df[OBJ_TOT] = np.array(custom_objective) + np.array(data_list.y)
        if elapsed_time is not None:
            self._hist_df[ELAPSED] = elapsed_time
        if is_de_duplication is not None:
            self._hist_df[DEDUP] = is_de_duplication

        self._num_initial_data = 0
        if num_initial_data is not None:
            self._num_initial_data = num_initial_data

    @property
    def num_initial_data(self) -> int:
        """The number of sample in the initial training data."""
        return self._num_initial_data

    @property
    def history_df(self) -> pd.DataFrame:
        """The history."""
        return self._hist_df
