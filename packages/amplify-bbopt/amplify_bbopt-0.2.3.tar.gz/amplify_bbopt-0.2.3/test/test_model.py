# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import amplify
import numpy as np
import pytest
import torch
from amplify_bbopt import ModelKernel, TorchFM


def test_torch_fm():
    seed = 0
    torch.manual_seed(seed)
    rng = np.random.default_rng(seed=seed)

    d_in = 10
    k_in = 20
    model = TorchFM(d=d_in, k=k_in)

    assert model._d == d_in  # noqa: SLF001
    assert model._k == k_in  # noqa: SLF001

    v, w, _ = model.parameters()
    assert len(v) == 10
    assert len(v[0]) == 20
    assert len(w) == 10
    q = amplify.VariableGenerator().array("Binary", 10)
    assert type(model.to_qubo(q)) is amplify.Poly

    out = model.forward(torch.Tensor(rng.random((3, len(v)))))
    assert len(out) == 3

    out = model.forward(torch.Tensor([range(len(v))]))
    assert out.item() == 287.8522644042969

    assert "TorchFM" in str(model)


def test_model_kernel():
    model = ModelKernel()
    with pytest.raises(RuntimeError) as _:
        # Error since no coefficient matrix is set.
        _ = model([1, 2, 3])

    q = amplify.VariableGenerator().array("Binary", 1)
    with pytest.raises(RuntimeError) as _:
        # Error since no coefficient matrix is set.
        _ = model.to_qubo(q)

    assert not model.is_sigma_required
    assert model.beta == 0
    assert model.gamma == 0.0

    coef_matrix = np.array([[0, 1, 2], [1, 1, 1], [2, 1, 1]], dtype=float)
    coef_vector = np.array([0, 1, 2], dtype=float)

    model.set_coefficient(coef_matrix)
    assert model([1, 2, 3]) == 41

    model = ModelKernel(gamma=1.0)
    model.set_coefficient(coef_matrix, coef_vector)
    assert model([1, 2, 3]) == 57
    assert model([[1, 2, 3], [-1, -2, -3]]) == [57, 25]

    q = amplify.VariableGenerator().array("Integer", 3, bounds=(1, 3))
    amplify_model = model.to_qubo(q)
    sol = {q[0]: 1.0, q[1]: 2.0, q[2]: 3.0}  # type: ignore
    assert amplify_model.substitute(sol) == 57  # type: ignore

    model = ModelKernel(beta=0, gamma=0)
    coef_matrix = np.array([[0, 1, 2], [1, 1, 1], [2, 1, 1]], dtype=float)
    model.set_coefficient(coef_matrix)
    assert model([1, 2, 3]) == 41

    model = ModelKernel(gamma=1)
    coef_matrix = np.array([[0, 1, 2], [1, 1, 1], [2, 1, 1]], dtype=float)
    model._coef_matrix_combined = coef_matrix  # noqa: SLF001
    # When gamma is, a coefficient vector must be set in such a case.
    with pytest.raises(RuntimeError) as _:
        _ = model([1, 2, 3])

    model = ModelKernel(beta=[0.0, 1.0], gamma=1.0)
    assert model.is_sigma_required
    assert model.beta == [0.0, 1.0]
    assert model.current_beta == 0.0

    km, ks = model.generate_kernel_functions()
    mat = np.array([1, 2])
    assert km(mat, mat) == 36
    assert ks(mat, mat) == 6

    beta = 1.0
    model = ModelKernel(beta=beta, gamma=1.0)
    assert model.is_sigma_required
    model.set_coefficient(coef_matrix, coef_vector, coef_matrix, coef_vector)
    assert (model.coef_matrix_mu == coef_matrix).all()
    assert (model.coef_vector_mu == coef_vector).all()
    assert (model.coef_matrix_sigma == np.eye(len(coef_matrix)) - (coef_matrix)).all()
    assert (model.coef_vector_sigma == coef_vector).all()
    assert (model.coef_matrix_combined == coef_matrix - beta * (np.eye(len(coef_matrix)) - (coef_matrix))).all()
    assert (model.coef_vector_combined == coef_vector - beta * coef_vector).all()

    assert "ModelKernel" in str(model)
