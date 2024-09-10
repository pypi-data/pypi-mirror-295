from __future__ import annotations

from abc import ABC, abstractmethod

import jax.numpy as jnp
import numpy as np
from sklearn.metrics import root_mean_squared_error

from JOPLEn.enums import LossType


def sigmoid(x: jnp.ndarray) -> jnp.ndarray:
    """Compute the sigmoid function element-wise.

    Args:
        x (jnp.ndarray): The input array.

    Returns:
        jnp.ndarray: The input array after applying the sigmoid function element-wise.
    """
    return jnp.reciprocal(1 + jnp.exp(-x))


class Loss(ABC):
    """A class that abstracts away the loss function, predictions, and gradient
    computations.
    """

    def __init__(self: Loss, loss_type: LossType) -> None:
        """Initializes the Loss class.

        Args:
            loss_type (LossType): What is the overall goal of the objective
                function? See the LossType enum in enums.py for more information.
        """
        self.loss_type = loss_type

    @abstractmethod
    def __call__(
        self: Loss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        y: jnp.ndarray,
        s: jnp.ndarray,
    ) -> float:
        """Computes the loss function.

        Args:
            w (jnp.ndarray): The weights of the model. Should have shape
                (n_features+1, n_partitions*n_cells) for linear cell models and
                (1, n_partitions*n_cells) for constant cell models.
            x (jnp.ndarray): The input features. Should have shape (n_samples,
                n_features+1) for linear cell models and (n_samples, 1)
                for constant cell models
            y (jnp.ndarray): The target values. Should have shape (n_samples, 1).
            s (jnp.ndarray): The assignment of each feature vector to a cell
                within each partition of the JOPLEn model. It is a binary matrix
                of shape (n_samples, n_partitions*n_cells).

        Returns:
            float: The loss value.
        """

    @abstractmethod
    def grad(
        self: Loss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        y: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        """Computes the gradient of the loss function.

        Args:
            w (jnp.ndarray): The weights of the model. Should have shape
                (n_features+1, n_partitions*n_cells) for linear cell models and
                (1, n_partitions*n_cells) for constant cell models.
            x (jnp.ndarray): The input features. Should have shape (n_samples,
                n_features+1) for linear cell models and (n_samples, 1)
                for constant cell models
            y (jnp.ndarray): The target values. Should have shape (n_samples, 1).
            s (jnp.ndarray): The assignment of each feature vector to a cell
                within each partition of the JOPLEn model. It is a binary matrix
                of shape (n_samples, n_partitions*n_cells).

        Returns:
            jnp.ndarray: The gradient of the loss function. Should have shape
                (n_features+1, n_partitions*n_cells) for linear cell models and
                (1, n_partitions*n_cells) for constant cell models
        """

    @abstractmethod
    def predict(
        self: Loss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        """Computes the predictions of the model, including any transformations
        such as link functions or discretization (e.g. classification).

        Args:
            w (jnp.ndarray): The weights of the model. Should have shape
                (n_features+1, n_partitions*n_cells) for linear cell models and
                (1, n_partitions*n_cells) for constant cell models.
            x (jnp.ndarray): The input features. Should have shape (n_samples,
                n_features+1) for linear cell models and (n_samples, 1)
                for constant cell models
            s (jnp.ndarray): The assignment of each feature vector to a cell
                within each partition of the JOPLEn model. It is a binary matrix
                of shape (n_samples, n_partitions*n_cells).

        Returns:
            jnp.ndarray: The predictions of the model.
        """

    def _raw_output(
        self: Loss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        """Computes the raw output of the model, i.e. the output before any
        transformations such as link functions or discretization.

        Args:
            w (jnp.ndarray): The weights of the model. Should have shape
                (n_features+1, n_partitions*n_cells) for linear cell models and
                (1, n_partitions*n_cells) for constant cell models.
            x (jnp.ndarray): The input features. Should have shape (n_samples,
                n_features+1) for linear cell models and (n_samples, 1)
                for constant cell models
            s (jnp.ndarray): The assignment of each feature vector to a cell
                within each partition of the JOPLEn model. It is a binary matrix
                of shape (n_samples, n_partitions*n_cells).

        Returns:
            jnp.ndarray: The raw output of the model.
        """
        return jnp.sum((x @ w) * s, axis=1, keepdims=True)

    @abstractmethod
    def error(
        self: Loss,
        y_true: np.ndarray,
        y_pred: np.ndarray,
    ) -> float:
        """Computes the error between the true and predicted values. This is used
        for settings where the loss is not the same as the true goal of the
        prediction task, such as classification accuracy for a logistic loss.
        In this setting, we measure error using classification accuracy, but the
        model is optimized using the logistic loss as a surrogate loss since it's
        easier to optimize.

        Args:
            y_true (np.ndarray): The true target values. Should have shape
                (n_samples, 1).
            y_pred (np.ndarray): The predicted target values. Should have shape
                (n_samples, 1).

        Returns:
            float: The error of the model.
        """


class SquaredError(Loss):
    def __init__(self: SquaredError) -> None:
        super().__init__(LossType.regression)

    def __call__(
        self: SquaredError,
        w: jnp.ndarray,
        x: jnp.ndarray,
        y: jnp.ndarray,
        s: jnp.ndarray,
    ) -> float:
        r"""Computes the squared error loss.

        Args:
            w (jnp.ndarray): The weights of the model. Should have shape
                (n_features+1, n_partitions*n_cells) for linear cell models and
                (1, n_partitions*n_cells) for constant cell models.
            x (jnp.ndarray): The input features. Should have shape (n_samples,
                n_features+1) for linear cell models and (n_samples, 1)
                for constant cell models
            y (jnp.ndarray): The target values. Should have shape (n_samples, 1).
                Should be in the range (-\infty, \infty).
            s (jnp.ndarray): The assignment of each feature vector to a cell
                within each partition of the JOPLEn model. It is a binary matrix
                of shape (n_samples, n_partitions*n_cells).

        Returns:
            float: The squared error loss.
        """
        y_pred = self.predict(w, x, s)

        return float(jnp.mean((y_pred - y) ** 2))

    def grad(
        self: SquaredError,
        w: jnp.ndarray,
        x: jnp.ndarray,
        y: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        r"""Computes the gradient of the squared error loss.

        Args:
            w (jnp.ndarray): The weights of the model. Should have shape
                (n_features+1, n_partitions*n_cells) for linear cell models and
                (1, n_partitions*n_cells) for constant cell models.
            x (jnp.ndarray): The input features. Should have shape (n_samples,
                n_features+1) for linear cell models and (n_samples, 1)
                for constant cell models
            y (jnp.ndarray): The target values. Should have shape (n_samples, 1).
                Should be in the range (-\infty, \infty).
            s (jnp.ndarray): The assignment of each feature vector to a cell
                within each partition of the JOPLEn model. It is a binary matrix
                of shape (n_samples, n_partitions*n_cells).

        Returns:
            jnp.ndarray: The gradient of the squared error loss. Should have shape
                (n_features+1, n_partitions*n_cells) for linear cell models and
                (1, n_partitions*n_cells) for constant cell models.
        """
        y_pred = self._raw_output(w, x, s)
        return x.T @ ((y_pred - y) * s) / x.shape[0]

    def predict(
        self: SquaredError,
        w: jnp.ndarray,
        x: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        """Computes the predictions of the model. In this case, it is the same
        as the raw output since no link function is used.

        Args:
            w (jnp.ndarray): The weights of the model. Should have shape
                (n_features+1, n_partitions*n_cells) for linear cell models and
                (1, n_partitions*n_cells) for constant cell models.
            x (jnp.ndarray): The input features. Should have shape (n_samples,
                n_features+1) for linear cell models and (n_samples, 1)
                for constant cell models
            s (jnp.ndarray): The assignment of each feature vector to a cell
                within each partition of the JOPLEn model. It is a binary matrix
                of shape (n_samples, n_partitions*n_cells).

        Returns:
            jnp.ndarray: The predictions of the model. Should have shape (n_samples, 1).
        """
        return self._raw_output(w, x, s)

    def error(
        self: SquaredError,
        y_true: np.ndarray,
        y_pred: np.ndarray,
    ) -> float:
        r"""Computes the root mean squared error between the true and predicted.

        Args:
            y_true (np.ndarray): The true target values. Should have shape
                (n_samples, 1). Should be in the range (-\infty, \infty).
            y_pred (np.ndarray): The predicted target values. Should have shape
                (n_samples, 1). Should be in the range (-\infty, \infty).

        Returns:
            float: The root mean squared error between the true and predicted values.
        """
        return float(root_mean_squared_error(y_true, y_pred))


class LogisticLoss(Loss):
    """A class that abstracts away the logistic loss function, predictions, and
    gradient computations."""

    def __init__(self: LogisticLoss) -> None:
        """Initializes the LogisticLoss class."""
        super().__init__(LossType.binary_classification)

    def encode(self: LogisticLoss, y: np.ndarray) -> np.ndarray:
        """Encodes the target values of 0 and 1 as -1 and 1 to make the computations
        more straightforward.

        Args:
            y (np.ndarray): The target values. Should have shape (n_samples, 1).

        Returns:
            np.ndarray: The encoded target values. Should have shape (n_samples, 1).
        """
        return (y * 2) - 1

    def __call__(
        self: LogisticLoss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        y: jnp.ndarray,
        s: jnp.ndarray,
    ) -> float:
        """Computes the logistic loss.

        Args:
            w (jnp.ndarray): The weights of the model. Should have shape
                (n_features+1, n_partitions*n_cells) for linear cell models and
                (1, n_partitions*n_cells) for constant cell models.
            x (jnp.ndarray): The input features. Should have shape (n_samples,
                n_features+1) for linear cell models and (n_samples, 1)
                for constant cell models
            y (jnp.ndarray): The target values. Should have shape (n_samples, 1).
                Should be values in {0, 1}.
            s (jnp.ndarray): The assignment of each feature vector to a cell
                within each partition of the JOPLEn model. It is a binary matrix
                of shape (n_samples, n_partitions*n_cells).

        Returns:
            float: The logistic loss.
        """

        raw_output = self._raw_output(w, x, s)
        y = self.encode(y)

        return float(jnp.mean(jnp.log(1 + jnp.exp(-y * raw_output))))

    def grad(
        self: LogisticLoss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        y: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        """Computes the gradient of the logistic loss.

        Args:
            w (jnp.ndarray): The weights of the model. Should have shape
                (n_features+1, n_partitions*n_cells) for linear cell models and
                (1, n_partitions*n_cells) for constant cell models.
            x (jnp.ndarray): The input features. Should have shape (n_samples,
                n_features+1) for linear cell models and (n_samples, 1)
                for constant cell models
            y (jnp.ndarray): The target values. Should have shape (n_samples, 1).
                Should be values in {0, 1}.
            s (jnp.ndarray): The assignment of each feature vector to a cell
                within each partition of the JOPLEn model. It is a binary matrix
                of shape (n_samples, n_partitions*n_cells).

        Returns:
            jnp.ndarray: The gradient of the logistic loss. Should have shape
                (n_features+1, n_partitions*n_cells) for linear cell models and
                (1, n_partitions*n_cells) for constant cell models.
        """
        raw_output = self._raw_output(w, x, s)
        y = self.encode(y)

        return -x.T @ ((y / (jnp.exp(raw_output * y) + 1)) * s) / x.shape[0]

    def predict(
        self: LogisticLoss,
        w: jnp.ndarray,
        x: jnp.ndarray,
        s: jnp.ndarray,
    ) -> jnp.ndarray:
        """Computes the predictions of the model using the sigmoid link function.

        Args:
            w (jnp.ndarray): The weights of the model. Should have shape
                (n_features+1, n_partitions*n_cells) for linear cell models and
                (1, n_partitions*n_cells) for constant cell models.
            x (jnp.ndarray): The input features. Should have shape (n_samples,
                n_features+1) for linear cell models and (n_samples, 1)
                for constant cell models
            s (jnp.ndarray): The assignment of each feature vector to a cell
                within each partition of the JOPLEn model. It is a binary matrix
                of shape (n_samples, n_partitions*n_cells).

        Returns:
            jnp.ndarray: The predictions of the model. Should have shape (n_samples,
            1) and be in [0, 1].
        """
        return sigmoid(self._raw_output(w, x, s))

    def error(
        self: LogisticLoss,
        y_true: np.ndarray,
        y_pred: np.ndarray,
    ) -> float:
        """Computes the error between the true and predicted values. In this case,
        the error is the classification accuracy.

        Args:
            y_true (np.ndarray): The true target values. Should have shape (n_samples, 1) and be in {0, 1}.
            y_pred (np.ndarray): The predicted target values. Should have shape (n_samples, 1) and be in [0, 1].

        Returns:
            float: _description_
        """
        return np.mean((y_true > 1 / 2) == (y_pred > 1 / 2))
