# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

import amplify
import numpy as np
import plotly.graph_objects as go

from .history import DEDUP, OBJ_TOT, History
from .logger import logger


def plot_history(history: History, log_scale: bool = False) -> go.Figure:
    """Show a plot of black-box optimization history.

    Args:
        history (History): The optimization history.
        log_scale (bool, optional): `True` for a y-log plot. Defaults to `False`. Defaults to False.

    Returns:
        go.Figure: Constructed Plotly figure
    """
    num_initial_data = history.num_initial_data
    history_df = history.history_df

    fig = go.Figure()

    # Plot corresponding to the data from the optimization cycles.
    fig.add_trace(
        go.Scatter(
            x=list(range(-num_initial_data + 1, len(history_df) - num_initial_data + 1)),
            y=history_df[OBJ_TOT],
            mode="lines",
            name="objective value",
            line={"color": "#999999", "dash": "solid"},
            opacity=0.8,
        )
    )

    # Plot corresponding to the data obtained purely from annealing.
    if DEDUP in history_df:
        plot_idx = np.where(1 - history_df[DEDUP].iloc[num_initial_data:])[0]
        x = plot_idx + 1
        y = [history_df[OBJ_TOT].iloc[i] for i in plot_idx + num_initial_data]

        fig.add_trace(
            go.Scatter(
                x=x,
                y=y,
                mode="markers",
                name="unique solution",
                line_color="#999999",
                marker={"symbol": "diamond-open", "size": 8, "line": {"width": 2}},
                opacity=0.8,
            )
        )

    # History of minimum objective function values.
    fig.add_trace(
        go.Scatter(
            x=list(range(-num_initial_data + 1, len(history_df) - num_initial_data + 1)),
            y=[history_df[OBJ_TOT].iloc[0]]
            + [min(history_df[OBJ_TOT].iloc[: i + 1]) for i in range(1, len(history_df))],
            mode="lines+markers",
            name="best objective",
            line={"color": "#E4001B", "width": 4},
        )
    )

    fig.add_vline(x=0, line_dash="dot", line_color="#555555")

    fig.update_layout(xaxis={"title": "number of cycles"}, yaxis={"title": "objective"})

    if log_scale:
        fig.update_yaxes(type="log")
    return fig


def anneal_history(result: amplify.Result) -> go.Figure | None:
    """Show annealing history of solutions.

    Solutions should be obtained by amplify.solve() with `amplify.FixstarsClient` with the `amplify.FixstarsClient.parameters.outputs.num_outputs = 0` slient setting. Compatible to non-unity `num_solves`.

    Args:
        result (amplify.Result): Annealing result returned from `amplify.FixstarsClient`.

    Returns:
        go.Figure | None: Constructed Plotly figure
    """  # noqa: E501
    if not isinstance(result.client_result, amplify.FixstarsClient.Result):
        return None
    fig = go.Figure()

    for i in range(result.num_solves):
        times = [solution.time.total_seconds() for solution in result.split[i]]
        objectives = [solution.objective for solution in result.split[i]]
        fig.add_trace(go.Scatter(x=times, y=objectives, mode="lines+markers", name=f"solve-{i}"))
    fig.update_layout(xaxis={"title": "elapsed time in seconds"}, yaxis={"title": "objective value"})
    logger().info(f"solver num iterations: {result.client_result.execution_parameters.num_iterations}")
    return fig
    return fig
