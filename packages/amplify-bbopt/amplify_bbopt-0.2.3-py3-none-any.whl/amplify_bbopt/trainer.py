# Copyright (c) Fixstars Amplify Corporation.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

from __future__ import annotations

import copy
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    import logging

    from torch.optim.optimizer import Optimizer

import numpy as np
import torch
from torch import nn
from torch.optim import lr_scheduler
from torch.optim.adamw import AdamW
from torch.utils.data import DataLoader, TensorDataset, random_split

from .misc import print_to_str, short_line
from .model import ModelKernel, TorchFM


class TrainerBase(ABC):
    """Base class for a surrogate/acquisiton function model trainer."""

    @abstractmethod
    def train(self, x_values: list[list[Any]], y_values: list[Any], logger: logging.Logger | None) -> Any:  # noqa: ANN401
        """Train a surrogate model.

        Args:
            x_values (list[list[Any]]): Input value vectors to the model.
            y_values (list[Any]): Output values corresponding to the input value vectors.
            logger (logging.Logger | None): A logger.

        Returns:
            Any: A trained model.
        """

    def init_seed(self, seed: int) -> None:  # noqa: B027
        """Initialize with a random seed.

        Args:
            seed (int): A random seed.
        """


class TorchFMTrainer(TrainerBase):
    """A trainer class for a Factorization Machine model implemented by PyTorch."""

    def __init__(self, model_class: type[TorchFM] = TorchFM) -> None:
        """Initialize the model trainer.

        By default :obj:`TorchFM` is considered and the default training parameters are set here by calling :obj:`TorchFMTrainer.set_train_params`.

        Args:
            model_class (Type[TorchFM]): A surrogate model class. By calling the constructor, default training parameters are set with :obj:`TorchFMTrainer.set_train_params`. Defaults to :obj:`TorchFM`.
        """  # noqa: E501
        self._model_class = model_class
        self._model_params: dict[str, Any] = {}
        # Set default training parameters (see all the parameters in set_train_params())
        self.set_train_params()

    def train(
        self,
        x_values: list[list[bool | int | float]],
        y_values: list[int | float],
        logger: logging.Logger | None = None,
    ) -> TorchFM:
        """Train an FM model (:obj:`TorchFM` or equivalent model class instance inheriting :obj:`TorchFM`).

        For adjustable training parameters, see :obj:`TorchFMTrainer.set_train_params`.

        Args:
            x_values (list[list[bool | int | float]]): A list of the input value vectors in the training data.
            y_values (list[int | float]): A list of the corresponding output values in the training data.
            logger (logging.Logger | None): A logger. Defaults to `None`.

        Returns:
            TorchFM: A trained FM model.
        """
        model = self._model_class(**self._model_params)

        optimizer = self._optimizer_class(model.parameters(), **self._optimizer_params)  # type: ignore
        criterion = self._loss_class()
        scheduler = None
        if self._lr_sche_class is not None:
            scheduler = self._lr_sche_class(optimizer, **self._lr_sche_params)  # type: ignore

        x_tensor, y_tensor = (
            torch.from_numpy(np.array(x_values)).float(),
            torch.from_numpy(np.array(y_values)).float(),
        )
        dataset = TensorDataset(x_tensor, y_tensor)

        split_ratio = self._data_split_ratio_train
        if int(len(y_values) * split_ratio) * int(len(y_values) * (1 - split_ratio)) == 0:
            # If self._data_split_ratio_train is 0 or 1, no data split is intentional
            # so the following warning is supressed.
            if split_ratio * (1 - split_ratio) > 0 and logger is not None:
                logger.warning("No data split is performed for this cycle.")
            train_set = dataset
            valid_set = dataset

        else:
            train_set, valid_set = random_split(  # type: ignore
                dataset, [self._data_split_ratio_train, 1 - self._data_split_ratio_train]
            )

        train_loader = DataLoader(train_set, batch_size=8, shuffle=True)
        valid_loader = DataLoader(valid_set, batch_size=8, shuffle=True)

        min_loss = 1e18
        best_parameters = copy.deepcopy(model.state_dict())
        for _ in range(self._epochs):
            # Training
            for x_train, y_train in train_loader:
                optimizer.zero_grad()
                out = model(x_train)
                loss = criterion(out, y_train)
                loss.backward()
                optimizer.step()

            # Validation
            with torch.no_grad():
                loss = 0
                for x_valid, y_valid in valid_loader:
                    y_pred = model(x_valid)
                    loss += criterion(y_pred, y_valid)
                # If the loss is updated, update the parameters
                if loss < min_loss:
                    best_parameters = copy.deepcopy(model.state_dict())
                    min_loss = loss
            if scheduler is not None:
                scheduler.step()

        # Make a model with the parameters with lowerst loss in validation
        with torch.no_grad():
            model.load_state_dict(best_parameters)
            model.eval()
            if logger is not None:
                logger.info(f"model corrcoef: {self._corrcoef(model, x_values, y_values):.3f}")  # noqa: G004
        return model

    def set_model_class(self, model_class: type[TorchFM]) -> None:
        """Set a model class.

        Args:
            model_class (Type[TorchFM]): An FM model class.
        """
        self._model_class = model_class

    @property
    def model_params(self) -> dict[str, Any] | None:
        """Model parameters the model class is initialized with."""
        return self._model_params

    @property
    def model_class(self) -> type[TorchFM]:
        """A model class considered in the training class."""
        return self._model_class

    @property
    def batch_size(self) -> int:
        """Batch size considered for training."""
        return self._batch_size

    @property
    def epochs(self) -> int:
        """The number of epochs for training."""
        return self._epochs

    @property
    def loss_class(self) -> type[torch.nn.modules.loss._Loss]:
        """A loss function class for model training."""
        return self._loss_class

    @property
    def optimizer_class(self) -> type[Optimizer]:
        """An optimizer class for model training."""
        return self._optimizer_class

    @property
    def optimizer_params(self) -> dict[str, Any]:
        """Optimizer parameters for model training."""
        return self._optimizer_params

    @property
    def lr_sche_class(self) -> type[lr_scheduler._LRScheduler] | None:
        """A learning rate scheduler class. If not used, return `None`."""
        return self._lr_sche_class

    @property
    def lr_sche_params(self) -> dict[str, Any] | None:
        """A learning rate scheduler parameters. If scheduler is not used, return `None`."""
        return self._lr_sche_params

    def set_model_params(self, **model_params: dict) -> None:
        """Set model parameters to be used to initialize the model class with (:obj:`TorchFM` by default).

        The following parameters can be set for the default model class (this overwrites the model parameters the optimizer set based on the observation of objective function):

        - d (int): The size of an FM input (= the number of the Amplify SDK variables fed to the model).
        - k (int): The FM hyperparameter. In :obj:`FMQAOptimizer` default to 10.
        """  # noqa: E501
        for k, v in model_params.items():
            self._model_params[k] = v

    def set_train_params(
        self,
        batch_size: int = 8,
        epochs: int = 2000,
        loss_class: type[torch.nn.modules.loss._Loss] = nn.MSELoss,
        optimizer_class: type[Optimizer] = AdamW,
        optimizer_params: dict[str, Any] | None = None,
        lr_sche_class: type[lr_scheduler._LRScheduler] | None = lr_scheduler.StepLR,  # type: ignore
        lr_sche_params: dict[str, Any] | None = None,
        data_split_ratio_train: float = 0.8,
        num_threads: int | None = None,
    ) -> None:
        """Set machine learning parameters.

        Args:
            batch_size (int, optional): A batch size. Defaults to 8.
            epochs (int, optional): A number of epochs. Defaults to 2000.
            loss_class (Type[torch.nn.modules.loss._Loss], optional): A loss function class. Defaults to `nn.MSELoss`.
            optimizer_class (Type[torch.optim.Optimizer], optional): An optimizer class. Defaults to `torch.optim.AdamW`.
            optimizer_params (Dict, optional): Optimization parameters. Defaults to `{"lr": 0.5}`.
            lr_sche_class (Type[lr_scheduler._LRScheduler] | None, optional): A learning rate scheduler class. Defaults to `lr_scheduler.StepLR`.
            lr_sche_params (Dict, optional): Learning rate scheduler parameters. Defaults to `{"step_size": 100, "gamma": 0.8}`.
            data_split_ratio_train (float, optional): Training dataset is split for training and validation. `data_split_ratio_train` defines the ratio of data used for traininig to the entire dataset samples. Note setting this either 0 or 1, training and validation use the same dataset (no split). Defaults to 0.8.
            num_threads (int | None, optional): The number of threads used for intraop parallel processing in PyTorch. If set `None`, available threads are used. Defaults to None.
        """  # noqa: E501
        self._batch_size = batch_size
        self._epochs = epochs
        self._loss_class = loss_class

        self._optimizer_class = optimizer_class
        if optimizer_params is None:
            self._optimizer_params = {"lr": 0.5}
        else:
            self._optimizer_params = optimizer_params

        self._lr_sche_class = lr_sche_class
        if lr_sche_params is None:
            self._lr_sche_params = {"step_size": 100, "gamma": 0.8}
        else:
            self._lr_sche_params = lr_sche_params

        self._data_split_ratio_train = data_split_ratio_train

        self._num_threads = num_threads
        if self._num_threads is not None:
            torch.set_num_threads(self._num_threads)

    def _corrcoef(
        self,
        trained_model: nn.Module,
        x_values: list[list[bool | int | float]],
        y_values: list[int | float],
    ) -> float:
        """Return a cross-correlation coefficient between the true values and values predicted by a model trained in this class.

        Args:
            trained_model (nn.Module): A trained FM model.
            x_values (list[list[bool | int | float]]): A list of the input value vectors (typically the same as the ones used for training in a black-box optimization context).
            y_values (list[int  |  float]): A list of output values corresponding to the input value vectors.

        Returns:
            float: The computed cross-correlation coefficient.
        """  # noqa: E501
        x_tensor = torch.from_numpy(np.array(x_values)).float()
        y_pred = trained_model(x_tensor).detach().numpy().ravel()
        return np.corrcoef(y_values, y_pred)[0, 1]

    def __str__(self) -> str:
        """Return human-readable training information.

        Returns:
            str: Training information.
        """
        ret = print_to_str(short_line)
        ret += print_to_str(f"trainer class: {self.__class__.__name__}")
        model = self.model_class(**self.model_params)  # type: ignore
        ret += print_to_str(model)
        ret += print_to_str(f"batch size: {self._batch_size}")
        ret += print_to_str(f"epochs: {self._epochs}")
        ret += print_to_str(f"loss class: {self._loss_class.__name__}")
        ret += print_to_str(f"optimizer class: {self._optimizer_class.__name__}")
        ret += print_to_str(f"optimizer params: {self._optimizer_params}")
        if self._lr_sche_class is not None:
            ret += print_to_str(f"lr_sche class: {self._lr_sche_class.__name__}")
            ret += print_to_str(f"lr_sche params: {self._lr_sche_params}")
        ret += print_to_str(f"data split ratio (train): {self._data_split_ratio_train}")
        return ret

    def init_seed(self, seed: int) -> None:
        """Initialize random with a seed.

        Args:
            seed (int): A seed.
        """
        np.random.seed(seed)  # noqa: NPY002
        torch.manual_seed(seed)


class GramMatrixHandler:
    """Compute and update the inverse of a Gram matrix sequentially with addition of a new data set."""

    def __init__(self, kernel_func: Callable, init_x: np.ndarray, reg_param: float) -> None:
        """Initialize a Gram matrix with the initial training data.

        Args:
            kernel_func (Callable): A kernel function for Gram matrix.
            init_x (np.ndarray): Input value vectors in the initial training data.
            reg_param (float): A regularization parameter.
        """
        self._kernel_func = kernel_func
        self._reg_param = reg_param
        self._inv_gram_matrix = self._calc_inv_gram_matrix(init_x)
        self._s: float = 0.0
        self._v: np.ndarray = np.array([])
        self._sum_vx: np.ndarray = np.array([])

    @property
    def inv_gram_matrix(self) -> np.ndarray:
        """The inverse of a Gram matrix."""
        return self._inv_gram_matrix

    @property
    def s(self) -> float:
        """The intermediate output scalar, s."""
        return self._s

    @property
    def v(self) -> np.ndarray:
        """The intermediate output vector, v."""
        return self._v

    @property
    def sum_vx(self) -> np.ndarray:
        """sum(x * v)."""
        return self._sum_vx

    def _calc_inv_gram_matrix(self, x: np.ndarray) -> np.ndarray:
        """Compute the inverse of a Gram matrix.

        Args:
            x (np.ndarray): Input value vectors in the initial training data.

        Returns:
             np.ndarray: Inverse of the Gram matrix.
        """
        k = self._kernel_func(x, x) + self._reg_param * np.eye(len(x))
        return np.linalg.inv(k)

    def update(self, x: np.ndarray) -> None:
        """Update a Gram matrix and related intermediate variables sequentially with addition of a new data set.

        Args:
            x (np.ndarray): Input value vectors in the training data (with the last element being a newly added input value vector).
        """  # noqa: E501
        x_new = x[-1, :]
        x_all_prev = x[: x.shape[0] - 1, :]
        kernel_vec = self._kernel_func(x_all_prev, x_new[None, :])
        kernel_n = self._kernel_func(x_new[None, :], x_new[None, :])
        self._s = (kernel_n + self._reg_param) - kernel_vec.T @ self._inv_gram_matrix @ kernel_vec
        self._v = self._inv_gram_matrix @ kernel_vec
        a = self._s * self._inv_gram_matrix + self._v @ self._v.T
        b = -self._v
        c = -self._v.T
        d = 1
        self._inv_gram_matrix = np.block([[a, b], [c, d]]) / self._s
        self._sum_vx = np.sum(x_all_prev * self._v, axis=0)


class PolyCoefMatrixHandler:
    """Compute and update polynomial coefficient matrices and vectors sequentially with addition of a new data set for the kernel-QA optimization."""  # noqa: E501

    def __init__(
        self,
        init_x: np.ndarray,
        init_y: np.ndarray,
        kernel_func_mu: Callable,
        kernel_func_sigma: Callable | None,
        reg_param: float,
        is_sigma_required: bool,
    ) -> None:
        """Initialize coefficient matrices and vectors with the initial training data.

        Args:
            init_x (np.ndarray): A list of the input value vectors in the initial training data.
            init_y (np.ndarray): Corresponding output values.
            kernel_func_mu (Callable): A kernel function for the mean.
            kernel_func_sigma (Callable | None): A kernel function for the sigma. When sigma is not considered throughout the optimization (`beta = 0` or `min(beta) = 0` in :obj:`ModelKernel`), set `None`.
            reg_param (float): A regularization parameter.
            is_sigma_required (bool): Whether the sigma is considered in the model (:obj:`ModelKernel` by default). See :obj:`ModelKernel.is_sigma_required`.
        """  # noqa: E501
        self._is_sigma_required = is_sigma_required
        self._gram_matrix_handler_mu = GramMatrixHandler(kernel_func_mu, init_x, reg_param)
        self._gram_matrix_handler_sigma: GramMatrixHandler | None = None

        # Initialize coef_matrix_mu (Q_mu)
        c_hat = self._gram_matrix_handler_mu.inv_gram_matrix @ init_y
        x_c_hat = init_x * c_hat[None, :].T
        self._coef_matrix_mu = x_c_hat.T @ init_x
        self._coef_vector_mu = x_c_hat.sum(axis=0)

        # Initialize coef_matrix_lxx for Q_sigma sequentially.
        num_samples = init_x.shape[0]
        size_input = init_x.shape[1]
        self._coef_matrix_lxx: np.ndarray | None = None
        self._coef_vector_sigma: np.ndarray | None = None
        if self._is_sigma_required:
            assert kernel_func_sigma is not None, "kernel_func_sigma must not be None when is_sigma_required is True."
            self._gram_matrix_handler_sigma = GramMatrixHandler(kernel_func_sigma, init_x, reg_param)
            inv_gram_matrix_sigma = self._gram_matrix_handler_sigma.inv_gram_matrix
            self._coef_matrix_lxx = np.zeros((size_input, size_input))
            self._coef_vector_sigma = np.zeros(size_input)
            for i in range(num_samples):
                for j in range(num_samples):
                    xi = init_x[i, :]
                    xj = init_x[j, :]
                    xx = xi[None, :].T @ xj[None, :]
                    self._coef_matrix_lxx += xx * inv_gram_matrix_sigma[i, j]
                    self._coef_vector_sigma += xi * inv_gram_matrix_sigma[i, j]
            self._coef_vector_sigma = (inv_gram_matrix_sigma @ init_x).sum(axis=0)

    @property
    def coef_matrix_mu(self) -> np.ndarray:
        return self._coef_matrix_mu

    @property
    def coef_vector_mu(self) -> np.ndarray:
        return self._coef_vector_mu

    @property
    def coef_matrix_lxx(self) -> np.ndarray | None:
        return self._coef_matrix_lxx

    @property
    def coef_vector_sigma(self) -> np.ndarray | None:
        return self._coef_vector_sigma

    def update(self, x: np.ndarray, y: np.ndarray) -> None:
        """Update polynomial coefficient matrices and vectors sequentially with addition of a new data set.

        Args:
            x (np.ndarray): All input value vectors in the training data (with the last element being a newly added input value vector).
            y (np.ndarray): Corresponding output values.
        """  # noqa: E501
        x_new = x[-1, :]
        # Update coef_matrix_lxx for Q_sigma sequentially.
        if self._is_sigma_required:
            assert self._gram_matrix_handler_sigma is not None
            self._gram_matrix_handler_sigma.update(x)
            sum_vx = self._gram_matrix_handler_sigma.sum_vx
            a1 = (sum_vx[None, :].T @ sum_vx[None, :]) / self._gram_matrix_handler_sigma.s
            a2 = (
                -sum_vx[None, :].T @ x_new[None, :] - x_new[None, :].T @ sum_vx[None, :]
            ) / self._gram_matrix_handler_sigma.s
            a3 = (x_new[None, :].T @ x_new[None, :]) / self._gram_matrix_handler_sigma.s
            self._coef_matrix_lxx += a1 + a2 + a3  # type: ignore
            self._coef_vector_sigma = (self._gram_matrix_handler_sigma.inv_gram_matrix @ x).sum(axis=0)

        # Update inv_gram_matrix and compute coef_matrix_mu (Q_mu).
        assert self._gram_matrix_handler_mu is not None
        self._gram_matrix_handler_mu.update(x)
        c_hat = self._gram_matrix_handler_mu.inv_gram_matrix @ y
        x_c_hat = x * c_hat[None, :].T
        self._coef_matrix_mu = x_c_hat.T @ x
        self._coef_vector_mu = x_c_hat.sum(axis=0)


class ModelKernelTrainer(TrainerBase):
    """A class for training a polynomial- and kernel-based surrogate model."""

    def __init__(self, model_class: type[ModelKernel] = ModelKernel) -> None:
        """Constructor.

        Args:
            model_class (Type[ModelKernel], optional): A model class to train. By calling the constructor, default training parameters are set with :obj:`ModelKernelTrainer.set_train_params`. Defaults to :obj:`ModelKernel`.
        """  # noqa: E501
        # Default setting for the model and training parameters
        self._model_class = model_class
        self._model_params: dict[str, Any] = {}
        self._reg_param: float | None = None
        self._beta: float | list[float] | None = None
        self._beta_array: np.ndarray | None = None

        self._matrix_handler: PolyCoefMatrixHandler | None = None
        self.set_train_params()

        self._i_cycle = 0

    def train(
        self, x_values: list[list[bool | int | float]], y_values: list[int | float], logger: logging.Logger | None
    ) -> ModelKernel:
        """Train a polynomial- and kernel-based model.

        Args:
            x_values (list[list[bool | int | float]]): A list of the input value vectors in the training data (with the last element being a newly added input value vector since the last training).
            y_values (list[int  |  float]): A list of the corresponding output values in the training data.
            logger (logging.Logger | None): A logger.

        Raises:
            RuntimeError: If a regularization parameter is not set.

        Returns:
            ModelKernel: A trained model.
        """  # noqa: E501
        if self._reg_param is None:
            raise RuntimeError("Regularization parameter must be set.")

        model = self._model_class(**self._model_params)

        x = np.array(x_values)
        y = np.array(y_values)
        if self._matrix_handler is None:
            kernel_mu, kernel_sigma = model.generate_kernel_functions()
            self._matrix_handler = PolyCoefMatrixHandler(
                x, y, kernel_mu, kernel_sigma, self._reg_param, model.is_sigma_required
            )
        else:
            self._matrix_handler.update(x, y)

        model.set_coefficient(
            matrix_mu=self._matrix_handler.coef_matrix_mu,
            vector_mu=self._matrix_handler.coef_vector_mu,
            matrix_lxx=self._matrix_handler.coef_matrix_lxx,
            vector_sigma=self._matrix_handler.coef_vector_sigma,
            i_cycle=self._i_cycle,
        )

        if logger is not None:
            logger.info(f"model corrcoef: {self._corrcoef(model, x_values, y_values):.3f}, beta: {model.current_beta}")  # noqa: G004

        self._i_cycle += 1
        return model

    def _corrcoef(
        self,
        trained_model: ModelKernel,
        x_values: list[list[bool | int | float]],
        y_values: list[int | float],
    ) -> float:
        """Return the cross-correlation coefficient between the true values and predicted values by a trained model.

        Args:
            trained_model (ModelKernel): A trained model.
            x_values (list[list[bool | int | float]]): A list of the input value vectors to predict.
            y_values (list[int | float]): A list of the corresponding output values.

        Returns:
            float: The cross-correlation coefficient.
        """
        y_pred = trained_model(x_values)

        return np.corrcoef(y_values, y_pred)[0, 1]

    def set_model_class(self, model_class: type[ModelKernel] = ModelKernel) -> None:
        """Set a model class.

        Args:
            model_class (Type[ModelKernel]): A model class. Defaults to :obj:`ModelKernel`.
        """
        self._model_class = model_class

    def set_model_params(self, **model_params: dict) -> None:
        """Set model parameters to initialize the model class with (:obj:`TorchFM` by default).

        The following parameters can be set for the default model class:

        - beta (float | list[float], optional): A weight for 'sigma' in the lower confidence bound (LCB). If multiple values of `beta` are given as a list, a value in the list is chosen and used in a cyclic manner each time the model is constructed (=in each optimization cycle). When `beta = 0` or `min(beta) = 0`, :obj:`ModelKernel.is_sigma_required = False`, meaning the model uncertainty is not considered. Defaults to 0.0.
        - gamma (float, optional): A constant in the kernel function to define a linear term in the model. `gamma = 0` means no linear term is considered in the model. Note that when the *a priori* encoding methods (()[conversion.ipynb]) are chosen for all decision variables, linear terms are expected to be modeled naturally in the quadratic terms. Defaults to 0.0.
        """  # noqa: E501
        for k, v in model_params.items():
            self._model_params[k] = v

    def set_train_params(self, reg_param: float = 1) -> None:
        """Set training parameters.

        Args:
            reg_param (float, optional): A regularization parameter. Defaults to 1.
        """
        self._reg_param = reg_param

    def __str__(self) -> str:
        """Return human-readable training information.

        Returns:
            str: Human-readable training information.
        """
        ret = print_to_str(short_line)
        ret += print_to_str(f"trainer class: {self.__class__.__name__}")
        model = self._model_class(**self._model_params)  # type: ignore
        ret += print_to_str(model)
        ret += print_to_str(f"reg_param: {self._reg_param}")
        return ret
