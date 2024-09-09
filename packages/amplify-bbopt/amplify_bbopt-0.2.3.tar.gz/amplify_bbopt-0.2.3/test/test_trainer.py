# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import numpy as np
from amplify_bbopt import PolyCoefMatrixHandler


def test_poly_coef_matrix_handler_no_linear_no_sigma():
    # common parameters
    reg_param = 1  # regularization parameters
    const = 0  # no linear term

    rng = np.random.default_rng(0)
    x_all = rng.random((100, 30))
    matrix_true = rng.random((30, 30))
    matrix_true += matrix_true.T
    y_all = np.diag(x_all @ matrix_true @ x_all.T)

    kernel_value_mu = (x_all @ x_all.T) ** 2
    c_hat = np.linalg.inv(kernel_value_mu + reg_param * np.eye(x_all.shape[0])) @ y_all
    x_c_hat = x_all * c_hat[None, :].T
    coef_matrix_mu_ref = x_c_hat.T @ x_all

    def kernel_func_mu(x, y):
        return (x @ y.T + const) ** 2

    # Construct coef_matrix_mu at once
    matrix_handler = PolyCoefMatrixHandler(x_all, y_all, kernel_func_mu, None, reg_param, False)
    assert (np.abs(coef_matrix_mu_ref - matrix_handler.coef_matrix_mu) < 1e-10).all()

    # Serially construct coef_matrix_mu
    init_x = x_all[:3]
    init_y = y_all[:3]
    matrix_handler = PolyCoefMatrixHandler(init_x, init_y, kernel_func_mu, None, reg_param, False)
    new_x = init_x
    new_y = init_y
    for i in range(3, x_all.shape[0]):
        new_x = np.append(new_x, x_all[i, :][None, :], axis=0)
        new_y = np.append(new_y, y_all[i])
        matrix_handler.update(new_x, new_y)
    assert (np.abs(coef_matrix_mu_ref - matrix_handler.coef_matrix_mu) < 1e-10).all()


def test_poly_coef_matrix_handler_with_linear_with_sigma():
    # common parameters
    reg_param = 1  # regularization parameters
    const = 1  # with linear term

    rng = np.random.default_rng(0)
    x_all = rng.random((100, 30))
    matrix_true = rng.random((30, 30))
    matrix_true += matrix_true.T
    vector_true = rng.random(30)
    y_all = np.diag(x_all @ matrix_true @ x_all.T) + x_all @ vector_true

    kernel_value_mu = (x_all @ x_all.T + const) ** 2
    c_hat = np.linalg.inv(kernel_value_mu + reg_param * np.eye(x_all.shape[0])) @ y_all
    x_c_hat = x_all * c_hat[None, :].T
    coef_matrix_mu_ref = x_c_hat.T @ x_all
    coef_vector_mu_ref = x_c_hat.sum(axis=0)

    kernel_value_sigma = x_all @ x_all.T
    inv_gram_matrix_sigma = np.linalg.inv(kernel_value_sigma + reg_param * np.eye(x_all.shape[0]))
    coef_matrix_lxx_ref = np.zeros((x_all.shape[1], x_all.shape[1]))
    for i in range(x_all.shape[0]):
        for j in range(x_all.shape[0]):
            xi = x_all[i, :]
            xj = x_all[j, :]
            xx = xi[None, :].T @ xj[None, :]
            coef_matrix_lxx_ref += (xx) * inv_gram_matrix_sigma[i, j]
    coef_vector_sigma_ref = (inv_gram_matrix_sigma @ x_all).sum(axis=0)

    def kernel_func_mu(x, y):
        return (x @ y.T + const) ** 2

    def kernel_func_sigma(x, y):
        return x @ y.T

    # Construct coef_matrix_mu, vector_mu, matrix_lxx (for sigma) at once
    matrix_handler = PolyCoefMatrixHandler(x_all, y_all, kernel_func_mu, kernel_func_sigma, reg_param, True)
    assert (np.abs(coef_matrix_mu_ref - matrix_handler.coef_matrix_mu) < 1e-10).all()
    assert (np.abs(coef_vector_mu_ref - matrix_handler.coef_vector_mu) < 1e-10).all()
    assert matrix_handler.coef_matrix_lxx is not None
    assert (np.abs(coef_matrix_lxx_ref - matrix_handler.coef_matrix_lxx) < 1e-10).all()

    # Serially construct coef_matrix_mu, vector_mu, matrix_lxx (for sigma)
    init_x = x_all[:3]
    init_y = y_all[:3]
    matrix_handler = PolyCoefMatrixHandler(init_x, init_y, kernel_func_mu, kernel_func_sigma, reg_param, True)
    new_x = init_x
    new_y = init_y
    for i in range(3, x_all.shape[0]):
        new_x = np.append(new_x, x_all[i, :][None, :], axis=0)
        new_y = np.append(new_y, y_all[i])
        matrix_handler.update(new_x, new_y)
    assert (np.abs(coef_matrix_mu_ref - matrix_handler.coef_matrix_mu) < 1e-10).all()
    assert (np.abs(coef_vector_mu_ref - matrix_handler.coef_vector_mu) < 1e-10).all()
    assert matrix_handler.coef_matrix_lxx is not None
    assert (np.abs(coef_matrix_lxx_ref - matrix_handler.coef_matrix_lxx) < 1e-10).all()
    assert (np.abs(coef_vector_sigma_ref - matrix_handler.coef_vector_sigma) < 1e-10).all()
