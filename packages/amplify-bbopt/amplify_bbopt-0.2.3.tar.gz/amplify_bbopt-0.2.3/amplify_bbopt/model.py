# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable

import amplify
import numpy as np
import torch
from torch import nn

from .misc import print_to_str


class QUBOConvertibleBase(ABC):
    """Base class for surrogate/acquisition function model class.

    A surrogate model class to be used with a QA-based black-box function solver must inherit this class.
    """

    @abstractmethod
    def to_qubo(self, x: amplify.PolyArray) -> amplify.Poly:
        """Convert the trained surrogate/acquisition function model to an Amplify SDK-compatible (QUBO) model.

        Args:
            x (amplify.PolyArray): The Amplify SDK's decision variables corresponding to the original variables for the black-box objective function that the surrogate/acquisition model tries to predict.

        Returns:
            amplify.Poly: The Amplify SDK-compatible model.
        """  # noqa: E501


class TorchFM(nn.Module, QUBOConvertibleBase):
    """Class to define a factorization machine implemented by PyTorch."""

    def __init__(self, d: int, k: int) -> None:
        """Initialize TorchFM class instance.

        Args:
            d (int): The size of an FM input (= the number of the Amplify SDK variables fed to the model).
            k (int): The FM hyperparameter.
        """
        super().__init__()
        self._d = d
        self._k = k
        self._v = torch.randn((d, k), requires_grad=True)
        self._w = torch.randn((d,), requires_grad=True)
        self._w0 = torch.randn((), requires_grad=True)

    def parameters(self, _: bool = True) -> list:  # type: ignore
        """Return a list of model parameters.

        Returns:
            list[torch.Tensor]: The list of model parameters, [v, w, w0].
        """
        return [self._v, self._w, self._w0]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Perform the forward pass of the model.

        Args:
            x (torch.Tensor): An input tensor with a shape (batch_size, d)

        Returns:
            torch.Tensor: The output tensor with a shape (batch_size, 1)
        """
        out_linear = torch.matmul(x, self._w) + self._w0
        out_1 = torch.matmul(x, self._v).pow(2).sum(1)
        out_2 = torch.matmul(x.pow(2), self._v.pow(2)).sum(1)
        out_quadratic = 0.5 * (out_1 - out_2)

        return out_linear + out_quadratic

    def _get_parameters(self) -> tuple[np.ndarray, np.ndarray, float]:
        """Return optimized model parameters.

        Returns:
            tuple[np.ndarray, np.ndarray, float]: Optimized parameters.
        """
        np_v = self._v.detach().numpy().copy()
        np_w = self._w.detach().numpy().copy()
        np_w0 = self._w0.detach().numpy().copy()
        return np_v, np_w, float(np_w0)

    def to_qubo(self, x: amplify.PolyArray) -> amplify.Poly:
        """Convert an FM model to the Amplify SDK-compatible QUBO based on the optimized FM parameters.

        Args:
            x (amplify.PolyArray): The Amplify SDK variables relevant to the :obj:`Variables` instance involved in the FM.

        Returns:
            amplify.Poly: The Amplify SDK's QUBO model.
        """  # noqa: E501
        v, w, w0 = self._get_parameters()

        out_linear = w0 + (x * w).sum()
        out_1 = ((x[:, np.newaxis] * v).sum(axis=0) ** 2).sum()  # type: ignore
        out_2 = ((x[:, np.newaxis] * v) ** 2).sum()
        objective: amplify.Poly = out_linear + (out_1 - out_2) / 2
        return objective

    def __str__(self) -> str:
        ret = print_to_str(f"model class: {self.__class__.__name__}")
        ret += print_to_str(f"model params: {{d: {self._d}, k: {self._k}}}")
        return ret


class ModelKernel(QUBOConvertibleBase):
    """Class to define a surrogate/acquisition function model based on second order polynomial kernels."""

    def __init__(self, beta: float | list[float] = 0.0, gamma: float = 0.0) -> None:
        """Initialize the kernel based model class.

        Args:
            beta (float | list[float], optional): A weight for 'sigma' in the lower confidence bound (LCB). If multiple values of `beta` are given as a list, a value in the list is chosen and used in a cyclic manner each time the model is constructed (=in each optimization cycle). When `beta = 0` or `min(beta) = 0`, :obj:`ModelKernel.is_sigma_required = False`, meaning the model uncertainty is not considered. Defaults to 0.0.
            gamma (float, optional): A constant in the kernel function to define a linear term in the model. `gamma = 0` means no linear term is considered in the model. Note that when the *a priori* encoding methods (()[conversion.ipynb]) are chosen for all decision variables, linear terms are expected to be modeled naturally in the quadratic terms. Defaults to 0.0.
        """  # noqa: E501
        self._coef_matrix_combined: np.ndarray | None = None
        self._coef_vector_combined: np.ndarray | None = None
        self._coef_matrix_mu: np.ndarray | None = None
        self._coef_vector_mu: np.ndarray | None = None
        self._coef_matrix_sigma: np.ndarray | None = None
        self._beta = beta
        if isinstance(self._beta, list):
            self._beta_array = np.array(self._beta)
        else:
            self._beta_array = np.array([self._beta])
        self._current_beta = self._beta_array[0]
        self._is_sigma_required = self._beta_array.max() > 0

        self._gamma = gamma

    def generate_kernel_functions(self) -> tuple[Callable, Callable]:
        """Generate polynomial kernel functions for k_mu (for mean) and k_sigma (for sigma).

        Returns:
            tuple[Callable, Callable]: The kernel functions, k_mu and k_sigma in a tuple in this order.
        """

        def kernel_func_mu(x, y):  # noqa: ANN001, ANN202
            return (x @ y.T + self._gamma) ** 2

        def kernel_func_sigma(x, y):  # noqa: ANN001, ANN202
            return x @ y.T + self._gamma

        return kernel_func_mu, kernel_func_sigma

    @property
    def is_sigma_required(self) -> bool:
        """Whether the sigma is considered in the model."""
        return self._is_sigma_required

    @property
    def gamma(self) -> float:
        """The gamma value for the kernel functions that corresponds to the linear terms in the model."""
        return self._gamma

    @property
    def beta(self) -> float | list[float]:
        """The beta value(s) for the sigma terms in LCB."""
        return self._beta

    @property
    def current_beta(self) -> float:
        """The value of `beta` used for the current model. When `beta` is given as a list in :obj:`ModelKernel.__init__`, a value in the list is chosen and used in a cyclic manner each time the model is constructed, and this value will be returned."""  # noqa: E501
        return self._current_beta

    @property
    def coef_matrix_mu(self) -> np.ndarray | None:
        """The coefficient matrix for the mean used for the current model. If the matrix is not set yet, return `None`."""  # noqa: E501
        return self._coef_matrix_mu

    @property
    def coef_matrix_sigma(self) -> np.ndarray | None:
        """The coefficient matrix for the sigma used for the current model. If the matrix is not set yet, return `None`."""  # noqa: E501
        return self._coef_matrix_sigma

    @property
    def coef_matrix_combined(self) -> np.ndarray | None:
        """The coefficient matrix combined for the mean and for sigma with `beta` used for the current model. If the matrix is not set yet, return `None`."""  # noqa: E501
        return self._coef_matrix_combined

    @property
    def coef_vector_mu(self) -> np.ndarray | None:
        """The coefficient vector for the mean used for the current model. If the vector is not set yet, return `None`."""  # noqa: E501
        return self._coef_vector_mu

    @property
    def coef_vector_sigma(self) -> np.ndarray | None:
        """The coefficient vector for sigma used for the current model. If the vector is not set yet, return `None`."""
        return self._coef_vector_sigma

    @property
    def coef_vector_combined(self) -> np.ndarray | None:
        """The coefficient vector combined for the mean and for sigma with `beta` used for the current model. If the vector is not set yet, return `None`."""  # noqa: E501
        return self._coef_vector_combined

    def set_coefficient(
        self,
        matrix_mu: np.ndarray,
        vector_mu: np.ndarray | None = None,
        matrix_lxx: np.ndarray | None = None,
        vector_sigma: np.ndarray | None = None,
        i_cycle: int = 0,
    ) -> None:
        """Update the model coefficient matrices and vectors.

        Args:
            matrix_mu (np.ndarray): The coefficient matrix for the mean
            vector_mu (np.ndarray | None, optional): The coefficient vector for the mean. This is required when `gamma > 0` is passed in :obj:`ModelKernel.__init__`. Defaults to `None`.
            matrix_lxx (np.ndarray | None, optional): The matrix (L_ij X X) to be used to construct the coefficient matrix for sigma. This is required when `current_beta > 0`. Defaults to `None`.
            vector_sigma (np.ndarray | None, optional): The coefficient vector for the sigma. This is required when `gamma > 0` and `current_beta > 0`. Defaults to `None`.
            i_cycle (int, optional): The cycle number from starting from 0 to be used for the cyclic `beta`. Defaults to 0.
        """  # noqa: E501
        if vector_mu is None:
            vector_mu = np.zeros(len(matrix_mu))
        if matrix_lxx is None:
            matrix_lxx = np.zeros(matrix_mu.shape)
        if vector_sigma is None:
            vector_sigma = np.zeros(len(matrix_mu))

        self._coef_matrix_mu = matrix_mu
        self._coef_vector_mu = vector_mu

        self._current_beta = self._beta_array[i_cycle % len(self._beta_array)]
        self._coef_matrix_sigma = None
        self._coef_vector_sigma = None

        self._coef_matrix_sigma = np.eye(matrix_lxx.shape[0]) - matrix_lxx
        self._coef_vector_sigma = vector_sigma
        self._coef_matrix_combined = self._coef_matrix_mu - self._current_beta * self._coef_matrix_sigma
        self._coef_vector_combined = self._coef_vector_mu - self._current_beta * self._coef_vector_sigma

    def to_qubo(self, x: amplify.PolyArray) -> amplify.Poly:
        """Convert a kernel-based model to the Amplify SDK-compatible QUBO based on the optimized FM parameters.

        Args:
            x (amplify.PolyArray): The Amplify SDK variables relevant to the :obj:`Variables` instance involved in the FM.

        Raises:
            RuntimeError: If the coefficient matrix combined for the mean and sigma is not set.

        Returns:
            amplify.Poly: The Amplify SDK's QUBO polynomial.
        """  # noqa: E501
        if self._coef_matrix_combined is None:
            raise RuntimeError("A coefficient matrix combined for the mean and sigma must be set.")

        ret = self._predict(x)
        assert isinstance(ret, amplify.Poly)
        return ret

    def _predict(self, x: np.ndarray | amplify.PolyArray) -> float | np.ndarray | amplify.Poly:
        """Perform prediction based on the current model.

        Args:
            x (np.ndarray | amplify.PolyArray): Input vector

        Raises:
            RuntimeError: If `gamma > 0` but the coefficient matrix combined for the mean and for sigma is `None` (not set).

        Returns:
            float | np.ndarray | amplify.Poly: a predicted value.
        """  # noqa: E501
        if self._gamma == 0:
            return x @ self._coef_matrix_combined @ x.T  # type: ignore
        quadratic = x @ self._coef_matrix_combined @ x.T  # type: ignore
        if self._coef_vector_combined is None:
            raise RuntimeError(
                "A coefficient vector combined for the mean and sigma must be set when gamma is non-zero."
            )
        linear = (self._coef_vector_combined[None, :] @ x.T).sum(axis=0)
        return quadratic + 2 * self._gamma * linear  # type: ignore

    def __call__(self, x: list[list[Any]] | list[Any]) -> list[float] | float:
        """Perform prediction based on the current model.

        Args:
            x (list[list[Any]] | list[Any]): An input vector or a list of input vectors.

        Raises:
            RuntimeError: If the coefficient matrix combined for the mean and for sigma is not set.

        Returns:
            list[float] | float: A predicted value or a list of the predicted values (in case of multiple input vectors are given).
        """  # noqa: E501
        if self._coef_matrix_combined is None:
            raise RuntimeError("A coefficient matrix combined for the mean and for sigma must be set.")

        if isinstance(x[0], list):
            ret = self._predict(np.array(x))
            assert isinstance(ret, np.ndarray)
            return np.diag(ret).tolist()

        ret = self._predict(np.array(x))
        assert isinstance(ret, (float, list))
        return ret

    def __str__(self) -> str:
        ret = print_to_str(f"model class: {self.__class__.__name__}")
        ret += print_to_str(f"model params: {{beta: {self.beta}, gamma: {self.gamma}}}")
        return ret
        return ret
