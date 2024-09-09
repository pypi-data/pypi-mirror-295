# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import logging
from datetime import timedelta
from typing import Annotated

import amplify
import numpy as np
import pytest
import torch
from amplify_bbopt import (
    BinaryVariableList,
    DataList,
    DatasetGenerator,
    FlatSolution,
    FMQAOptimizer,
    IntegerVariable,
    IntegerVariableList,
    KernelQAOptimizer,
    MultiObjectiveOptimizer,
    StructuredSolution,
    TorchFMTrainer,
    blackbox,
    equal_to,
    logger,
)


@blackbox
def objective_func_1(
    x: Annotated[list[bool], BinaryVariableList(length=3)],
):
    return sum(x)


@blackbox
def objective_func_2(
    x: Annotated[list[bool], BinaryVariableList(length=3)],
    a: Annotated[int, IntegerVariable(bounds=(0, 3))],
):
    return sum(x) + a


@blackbox
def objective_func_3(
    y: Annotated[list[bool], BinaryVariableList(length=3)],
    b: Annotated[int, IntegerVariable(bounds=(0, 3))],
):
    return sum(y) + b


@blackbox
def objective_func_4(
    x: Annotated[list[int], IntegerVariableList(bounds=(0, 9), length=3)],
    c: Annotated[int, IntegerVariable(bounds=(0, 19))],
):
    return sum(x) + c


assert logger.handler is not None
logger.handler.setLevel(logging.ERROR)


@pytest.fixture
def fmqa_optimizer(require_client=True):
    client = None
    if require_client:
        client = amplify.FixstarsClient()
        client.parameters.timeout = timedelta(milliseconds=1000)  # 1000 ミリ秒
        # client.token = ""
    data = DatasetGenerator(objective=objective_func_1, seed=0).generate(num_samples=3)
    assert isinstance(data, DataList)
    return FMQAOptimizer(data, objective_func_1, client, seed=0)


@pytest.fixture
def kernel_qa_optimizer(require_client=True):
    client = None
    if require_client:
        client = amplify.FixstarsClient()
        client.parameters.timeout = timedelta(milliseconds=1000)  # 1000 ミリ秒
        # client.token = ""
    data = DatasetGenerator(objective=objective_func_2, seed=0).generate(num_samples=3)
    assert isinstance(data, DataList)
    return KernelQAOptimizer(data, objective_func_2, client, seed=0)


@pytest.fixture
def kernel_qa_optimizer_sub(require_client=True):
    client = None
    if require_client:
        client = amplify.FixstarsClient()
        client.parameters.timeout = timedelta(milliseconds=1000)  # 1000 ミリ秒
        # client.token = ""
    data = DatasetGenerator(objective=objective_func_3, seed=0).generate(num_samples=3)
    assert isinstance(data, DataList)
    return KernelQAOptimizer(data, objective_func_3, client, seed=0)


@pytest.fixture
def kernel_qa_optimizer_4(require_client=True):
    client = None
    if require_client:
        client = amplify.FixstarsClient()
        client.parameters.timeout = timedelta(milliseconds=1000)  # 1000 ミリ秒
        # client.token = ""
    data = DatasetGenerator(objective=objective_func_4, seed=0).generate(num_samples=3)
    assert isinstance(data, DataList)
    return KernelQAOptimizer(data, objective_func_4, client, seed=0)


def test_ensure_uniqueness_single_objective(kernel_qa_optimizer_4):
    rng = np.random.default_rng(seed=0)

    num_tests = 10
    ave_distance = 0.0

    for _i in range(num_tests):
        idx = rng.integers(low=0, high=len(kernel_qa_optimizer_4.data))
        solution = FlatSolution(
            kernel_qa_optimizer_4.objective.variables, kernel_qa_optimizer_4.data.x[idx]
        ).to_structured()
        org_solution = solution.copy()
        solution, _is_modified = kernel_qa_optimizer_4._ensure_uniqueness(solution, 10)  # noqa: SLF001
        ave_distance += np.sqrt(
            ((np.array(org_solution.to_flat().values) - np.array(solution.to_flat().values)) ** 2).sum()
        )
    ave_distance /= num_tests
    print(f"{ave_distance=}")


def test_fmqa_optimizer(fmqa_optimizer):
    poly_array = fmqa_optimizer.objective.variables.poly_array
    custom_obj = poly_array[0] * poly_array[1]
    fmqa_optimizer.custom_objective = custom_obj
    assert fmqa_optimizer.custom_objective == poly_array[0] * poly_array[1]
    assert isinstance(fmqa_optimizer.trainer, TorchFMTrainer)

    assert fmqa_optimizer.i_cycle == 0

    var_x = fmqa_optimizer.objective.variables.x
    fmqa_optimizer.custom_amplify_objective = var_x[0] * var_x[1]
    fmqa_optimizer.custom_amplify_objective = None

    assert fmqa_optimizer.num_initial_data == 3
    fmqa_optimizer.data.append(([True, False, True], 2))
    fmqa_optimizer.num_initial_data = 4

    with pytest.raises(ValueError) as _:
        # elapse_time and is_de_duplication do not have the same length as optimizer._data.
        _ = fmqa_optimizer.fetch_history()

    fmqa_optimizer._elapsed_time.append(0)  # noqa: SLF001
    fmqa_optimizer._is_de_duplication.append(True)  # noqa: SLF001
    history = fmqa_optimizer.fetch_history()
    print(history.history_df)

    assert len(history.history_df) == 4
    assert history.num_initial_data == 4

    x0 = FlatSolution(fmqa_optimizer.objective.variables, fmqa_optimizer.data.x[0]).to_structured().copy()

    sol, is_modified = fmqa_optimizer._ensure_uniqueness(x0, 10)  # noqa: SLF001
    assert sol.values != x0.values
    assert is_modified

    x0 = FlatSolution(fmqa_optimizer.objective.variables, fmqa_optimizer.data.x[0]).to_structured().copy()
    sol, is_modified = fmqa_optimizer._ensure_uniqueness(x0, 0)  # noqa: SLF001
    assert sol.values == x0.values
    assert not is_modified

    x = [1, 0, 1]
    solution = StructuredSolution(fmqa_optimizer.objective.variables, x=[x])
    solution_dict = {fmqa_optimizer.objective.variables.poly_array[i]: x[i] for i in range(len(x))}

    assert fmqa_optimizer._evaluate_objective_func(solution) == sum(x)  # noqa: SLF001
    assert fmqa_optimizer.surrogate_model is None
    assert fmqa_optimizer.amplify_model is None

    fmqa_optimizer.optimize(num_cycles=1)

    assert fmqa_optimizer.surrogate_model is not None
    out_fm = fmqa_optimizer.surrogate_model(torch.Tensor([x]))[0].item()
    assert fmqa_optimizer.amplify_model is not None
    out_qubo = float(fmqa_optimizer.amplify_model.objective.substitute(solution_dict))
    assert round(out_fm, 5) == round(out_qubo, 5)

    assert "x" in fmqa_optimizer.best_solution


def test_multi_objective_optimizer_dependency_variables_unification(fmqa_optimizer, kernel_qa_optimizer):
    # two objective functions dependent via a common variable x.
    # test to correctly unify the variables.

    assert (
        fmqa_optimizer.objective.variables.amplify_variables["x"] == fmqa_optimizer.objective.variables.poly_array
    ).all()

    optimizer_multi = MultiObjectiveOptimizer([fmqa_optimizer, kernel_qa_optimizer], fmqa_optimizer._client)  # noqa: SLF001

    length = len(optimizer_multi.objectives[1].variables.poly_array)

    assert (
        optimizer_multi.objectives[0].variables.poly_array
        == optimizer_multi.objectives[1].variables.poly_array[: length - 3]
    ).all()

    assert (
        optimizer_multi.objectives[0].variables.amplify_variables["x"]
        == optimizer_multi.objectives[1].variables.amplify_variables["x"]
    ).all()  # type: ignore


def test_multi_objective_optimizer_dependency_constraint_unification(fmqa_optimizer, kernel_qa_optimizer_sub):
    # two objective functions dependent via constraint that relates
    # a variable of one objective to a variable of another objective.
    # test to correctly unify the variables.

    assert (
        fmqa_optimizer.objective.variables.amplify_variables["x"] == fmqa_optimizer.objective.variables.poly_array
    ).all()

    optimizer_multi = MultiObjectiveOptimizer([fmqa_optimizer, kernel_qa_optimizer_sub], fmqa_optimizer._client)  # noqa: SLF001

    x = fmqa_optimizer.objective.variables.x
    y = kernel_qa_optimizer_sub.objective.variables.y

    c = equal_to(x.sum() - y.sum(), 0)  # x = y
    kernel_qa_optimizer_sub.objective.add_constraint(c)

    length = len(optimizer_multi.objectives[1].variables.poly_array)
    assert not (
        optimizer_multi.objectives[0].variables.poly_array
        == optimizer_multi.objectives[1].variables.poly_array[: length - 3]
    ).all()

    sol_fmqa = StructuredSolution(fmqa_optimizer.objective.variables, [[True, False, False]])
    sol_kernel = StructuredSolution(kernel_qa_optimizer_sub.objective.variables, [[True, False, False], 0])
    flat_sol_dict = optimizer_multi._combine_solutions([sol_fmqa, sol_kernel])  # noqa: SLF001
    assert optimizer_multi._is_satisfied(flat_sol_dict)  # noqa: SLF001

    sol_fmqa = StructuredSolution(fmqa_optimizer.objective.variables, [[True, True, False]])
    sol_kernel = StructuredSolution(kernel_qa_optimizer_sub.objective.variables, [[True, False, False], 0])
    flat_sol_dict = optimizer_multi._combine_solutions([sol_fmqa, sol_kernel])  # noqa: SLF001
    assert not optimizer_multi._is_satisfied(flat_sol_dict)  # noqa: SLF001


def test_multi_objective_optimizer(fmqa_optimizer, kernel_qa_optimizer):
    optimizer_multi = MultiObjectiveOptimizer([fmqa_optimizer, kernel_qa_optimizer], fmqa_optimizer._client)  # noqa: SLF001

    poly_array = optimizer_multi.objectives[1].variables.poly_array
    custom_obj = poly_array[0] * poly_array[3]
    optimizer_multi.custom_amplify_objective = custom_obj
    assert optimizer_multi.custom_amplify_objective == poly_array[0] * poly_array[3]

    assert optimizer_multi.best_objective is None
    assert optimizer_multi.best_solution is None

    optimizer_multi.optimize(num_cycles=1)

    assert optimizer_multi.best_solution is not None
    a = optimizer_multi.best_solution.pop("a")
    assert optimizer_multi.best_objective == objective_func_1(
        list(optimizer_multi.best_solution.values())
    ) + objective_func_2(x=list(optimizer_multi.best_solution.values()), a=a)  # type: ignore
    assert optimizer_multi.i_cycle == 0
    assert len(optimizer_multi.data) == 1
