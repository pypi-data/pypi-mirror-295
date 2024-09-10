from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any

import jax.numpy as jnp
import numpy as np

from .enums import DTYPE
from .partitioner import Partitioner, TreePartition
from .proj_l1_ball import euclidean_proj_l1ball


class Penalty(ABC):
    """Base class for implementing regularization penalties for JOPLEn."""

    def __init__(
        self: Penalty,
        is_smooth: bool,
    ) -> None:
        """Initializes the penalty object.

        Args:
            is_smooth (bool): Whether the penalty is smooth or not. This is used
            to determine whether we should use the gradient or proximal operator.
        """
        self.is_smooth = is_smooth

    def build(  # noqa: B027
        self: Penalty,
        x_train: np.ndarray,
        x_val: np.ndarray,
        partitioner: Partitioner,
    ) -> None:
        """Perform any necessary precomputation for the penalty to reduce
        redundant computation during training.

        Args:
            x_train (np.ndarray): The features of the training data. Used for
                the lapalacian penalty. Should have shape (n_train, n_features).
            x_val (np.ndarray): The features of the validation data. Should have
                shape (n_val, n_features).
            partitioner (Partitioner): The partitioner object. Used for certain
                laplacian penalties.
        """

    @abstractmethod
    def __call__(
        self: Penalty,
        w: jnp.ndarray,
        bias_idx: int | None,
        x: jnp.ndarray,
        y_pred: jnp.ndarray,
        s: jnp.ndarray,
        is_train: bool,
    ) -> float:
        """Computes the penalty value.

        Args:
            w (jnp.ndarray): The weights of the JOPLEn model.
            bias_idx (int | None): The index of the bias term in the weights. Used to
                remove the bias term from the penalty if using a linear leaf model.
                Should have shape (n_features+1, n_partitions*n_cells) for the
                linear model and (1, n_partitions*n_cells) for the constant model.
            x (jnp.ndarray): The features of the data. Should have shape
                (n_data_points, n_features+1).
            y_pred (jnp.ndarray): The predicted response values. Should have shape
                (n_data_points, 1).
            s (jnp.ndarray): The partition mask for the data. Indicates which
                partition and cell each data point belongs to. Should have shape
                (n_data_points, n_partitions*n_cells).
            is_train (bool): Whether the penalty is being computed for the training
                or validation data. Some penalties may have different behavior for
                training and validation data.

        Returns:
            float: The computed penalty value.
        """

    def grad(
        self: Penalty,
        mu: float,
        w: jnp.ndarray,
        bias_idx: int | None,
        x: jnp.ndarray,
        y_pred: jnp.ndarray,
        s: jnp.ndarray,
        is_train: bool,
    ) -> jnp.ndarray:
        """Computes the gradient of the penalty.

        Args:
            mu (float): The step size for the gradient update.
            w (jnp.ndarray): The weights of the JOPLEn model. Should have shape
                (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
            bias_idx (int | None): The index of the bias term in the weights. Used
                to remove the bias term from the penalty if using a linear model.
            x (jnp.ndarray): The features of the data. Should have shape
                (n_data_points, n_features+1) for the linear model and (n_data_points,
                1) for the constant model.
            y_pred (jnp.ndarray): The predicted response values. Should have shape
                (n_data_points, 1).
            s (jnp.ndarray): The partition mask for the data. Indicates which
                partition and cell each data point belongs to. Should have shape
                (n_data_points, n_partitions*n_cells).
            is_train (bool): Whether the penalty is being computed for the training
                or validation data. Some penalties may have different behavior for
                training and validation data.

        Raises:
            NotImplementedError: If the user doesn't overload this method, then
                the loss is assumed to be non-smooth.

        Returns:
            jnp.ndarray: The gradient to be applied to the weights. Should have
                shape (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model
        """
        raise NotImplementedError(
            "Gradient is not implemented, probably because the penalty is not smooth."
        )

    def prox(
        self: Penalty,
        mu: float,
        w: jnp.ndarray,
        bias_idx: int | None,
        x: jnp.ndarray,
        y_pred: jnp.ndarray,
        s: jnp.ndarray,
        is_train: bool,
    ) -> jnp.ndarray:
        """Computes the proximal operator of the penalty and applies it to the
            weight matrix.

        Args:
            mu (float): The step size for the proximal operator.
            w (jnp.ndarray): The weights of the JOPLEn model. Should have shape
                (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
            bias_idx (int | None): The index of the bias term in the weights. Used
                to remove the bias term from the penalty if using a linear model.
            x (jnp.ndarray): The features of the data. Should have shape
                (n_data_points, n_features+1) for the linear model and (n_data_points,
            y_pred (jnp.ndarray): The predicted response values. Should have shape
                (n_data_points, 1).
            s (jnp.ndarray): The partition mask for the data. Indicates which
                partition and cell each data point belongs to. Should have shape
                (n_data_points, n_partitions*n_cells).
            is_train (bool): Whether the penalty is being computed for the training
                or validation data. Some penalties may have different behavior for
                training and validation data.

        Raises:
            NotImplementedError: If the user doesn't overload this method, then
                the loss is assumed to be smooth.

        Returns:
            jnp.ndarray: The weights after applying the proximal operator. Should
                have shape (n_features+1, n_partitions*n_cells) for the linear model
                and (1, n_partitions*n_cells) for the constant model.
        """
        raise NotImplementedError(
            "Proximal operator is not implemented, probably because the penalty is smooth."
        )


class SquaredFNorm(Penalty):
    """A squared Frobenius norm penalty."""

    def __init__(
        self: SquaredFNorm,
        lam: float = 1.0,
    ) -> None:
        """Initializes the squared Frobenius norm penalty.

        Args:
            lam (float, optional): Regularization parameter. Defaults to 1.0.
        """
        super().__init__(is_smooth=True)

        assert lam > 0, "The regularization parameter must be positive."
        self.lam = lam

    def __call__(
        self: SquaredFNorm,
        w: jnp.ndarray,
        bias_idx: int | None,
        *_: list,
    ) -> float:
        """Computes the weighted penalty value.

        Args:
            w (jnp.ndarray): The weights of the JOPLEn model. Should have shape
                (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
            bias_idx (int | None): The index of the bias term in the weights.
                Used to remove the bias term from the penalty if using a linear
                model.

        Returns:
            float: The computed weighted penalty value.
        """
        return self.lam * jnp.sum(w[:bias_idx] ** 2) / 2

    def grad(
        self: SquaredFNorm,
        mu: float,
        w: jnp.ndarray,
        bias_idx: int | None,
        *_: list,
    ) -> jnp.ndarray:
        """Computes the gradient of the penalty.

        Args:
            mu (float): The step size for the gradient update. Included because
                the proximal operator requires it and we want to keep the interface
                consistent.
            w (jnp.ndarray): The weights of the JOPLEn model. Should have shape
                (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
            bias_idx (int | None): The index of the bias term in the weights.
                Used to remove the bias term from the penalty if using a linear
                model.

        Returns:
            jnp.ndarray: The gradient to be applied to the weights. Should have
                shape (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
        """
        grad_out = jnp.zeros_like(w)
        return grad_out.at[:bias_idx].set(self.lam * mu * w[:bias_idx])


class NonsmoothGroupPenalty(Penalty, ABC):
    """Base class for implementing nonsmooth group penalties for JOPLEn. Mainly
    used to simplify the implementation of nonsmooth penalties.
    """

    def __init__(
        self: NonsmoothGroupPenalty,
        lam: float = 1.0,
    ) -> None:
        """Initializes the nonsmooth group penalty.

        Args:
            lam (float, optional): The penalty weight. Defaults to 1.0.
        """
        super().__init__(is_smooth=False)

        assert lam > 0, "The regularization parameter must be positive."
        self.lam = lam


class Group21Norm(NonsmoothGroupPenalty):
    r"""The \ell_{2,1} group norm penalty."""

    def __call__(
        self: Group21Norm,
        w: jnp.ndarray,
        bias_idx: int | None,
        *_: list,
    ) -> float:
        """Computes the weighted penalty value.

        Args:
            w (jnp.ndarray): The weights of the JOPLEn model. Should have shape
                (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
            bias_idx (int | None): The index of the bias term in the weights.
                Used to remove the bias term from the penalty if using a linear
                model.

        Returns:
            float: The computed weighted penalty value.
        """
        return jnp.linalg.norm(w[:bias_idx], axis=-1, ord=2).sum()

    def prox(
        self: Group21Norm,
        mu: float,
        w: jnp.ndarray,
        bias_idx: int | None,
        *_: list,
    ) -> jnp.ndarray:
        """Computes the proximal operator of the penalty and applies it to the
        weight matrix.

        Args:
            mu (float): The step size for the proximal operator.
            w (jnp.ndarray): The weights of the JOPLEn model. Should have shape
                (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
            bias_idx (int | None): The index of the bias term in the weights.
                Used to remove the bias term from the penalty if using a linear
                model.

        Returns:
            jnp.ndarray: The weights after applying the proximal operator. Should
                have shape (n_features+1, n_partitions*n_cells) for the linear model
                and (1, n_partitions*n_cells) for the constant model.
        """
        norm = jnp.linalg.norm(w[:bias_idx], axis=1, keepdims=True, ord=2)
        return w.at[:bias_idx].set(
            w[:bias_idx] * jnp.maximum(1 - self.lam * mu / norm, 0)
        )


class GroupInf1Norm(NonsmoothGroupPenalty):
    r"""The \ell_{\infty,1} group norm penalty."""

    def __call__(
        self: GroupInf1Norm,
        w: jnp.ndarray,
        bias_idx: int | None,
        *_: list,
    ) -> float:
        """Computes the weighted penalty value.

        Args:
            w (jnp.ndarray): The weights of the JOPLEn model. Should have shape
                (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
            bias_idx (int | None): The index of the bias term in the weights.
                Used to remove the bias term from the penalty if using a linear
                model.

        Returns:
            float: The computed weighted penalty value.
        """
        return jnp.sum(jnp.max(jnp.abs(w[:bias_idx]), axis=-1))

    def prox(
        self: GroupInf1Norm,
        mu: float,
        w: jnp.ndarray,
        bias_idx: int | None,
        *_: list,
    ) -> jnp.ndarray:
        """Computes the proximal operator of the penalty and applies it to the
        weight matrix.

        Args:
            mu (float): The step size for the proximal operator.
            w (jnp.ndarray): The weights of the JOPLEn model. Should have shape
                (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
            bias_idx (int | None): The index of the bias term in the weights.
                Used to remove the bias term from the penalty if using a linear
                model.

        Returns:
            jnp.ndarray: The weights after applying the proximal operator. Should
                have shape (n_features+1, n_partitions*n_cells) for the linear model
                and (1, n_partitions*n_cells) for the constant model.
        """
        w = w.at[:bias_idx].set(
            -self.lam * mu * euclidean_proj_l1ball(w[:bias_idx] / self.lam * mu)
        )

        return w


class NuclearNorm(NonsmoothGroupPenalty):
    """The nuclear norm penalty."""

    def __call__(
        self: NuclearNorm,
        w: jnp.ndarray,
        bias_idx: int | None,
        *_: list,
    ) -> float:
        """Computes the weighted penalty value.

        Args:
            w (jnp.ndarray): The weights of the JOPLEn model. Should have shape
                (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
            bias_idx (int | None): The index of the bias term in the weights.
                Used to remove the bias term from the penalty if using a linear
                model.

        Returns:
            float: The computed weighted penalty value.
        """
        s = jnp.linalg.svd(w[:bias_idx], full_matrices=True, compute_uv=False)
        return jnp.sum(s)

    def prox(
        self: NuclearNorm,
        mu: float,
        w: jnp.ndarray,
        bias_idx: int | None,
        *_: list,
    ) -> jnp.ndarray:
        """Computes the proximal operator of the penalty and applies it to the
        weight matrix.

        Args:
            mu (float): The step size for the proximal operator.
            w (jnp.ndarray): The weights of the JOPLEn model. Should have shape
                (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
            bias_idx (int | None): The index of the bias term in the weights.
                Used to remove the bias term from the penalty if using a linear
                model.

        Returns:
            jnp.ndarray: The weights after applying the proximal operator. Should
                have shape (n_features+1, n_partitions*n_cells) for the linear model
                and (1, n_partitions*n_cells) for the constant model.
        """
        u, s, v = jnp.linalg.svd(w[:bias_idx], full_matrices=False)
        s = jnp.maximum(s - self.lam * mu, 0)
        return w.at[:bias_idx].set(u @ (s[:, None] * v))


class L1Norm(Penalty):
    r"""The \ell_1 norm penalty."""

    def __init__(
        self: L1Norm,
        lam: float = 1.0,
    ) -> None:
        r"""Initializes the \ell_1 norm penalty.

        Args:
            lam (float, optional): The penalty weight. Defaults to 1.0.
        """
        super().__init__(is_smooth=False)

        assert lam > 0, "The regularization parameter must be positive."
        self.lam = lam

    def __call__(
        self: L1Norm,
        w: jnp.ndarray,
        bias_idx: int | None,
        *_: list,
    ) -> float:
        """Computes the weighted penalty value.

        Args:
            w (jnp.ndarray): The weights of the JOPLEn model. Should have shape
                (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
            bias_idx (int | None): The index of the bias term in the weights.
                Used to remove the bias term from the penalty if using a linear
                model.

        Returns:
            float: The computed weighted penalty value.
        """
        return self.lam * jnp.sum(jnp.abs(w[:bias_idx]))

    def prox(
        self: L1Norm,
        mu: float,
        w: jnp.ndarray,
        bias_idx: int | None,
        *_: list,
    ) -> jnp.ndarray:
        """Computes the proximal operator of the penalty and applies it to the
        weight matrix.

        Args:
            mu (float): The learning rate for the proximal operator.
            w (jnp.ndarray): The weights of the JOPLEn model. Should have shape
                (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
            bias_idx (int | None): The index of the bias term in the weights.

        Returns:
            jnp.ndarray: The weights after applying the proximal operator. Should
                have shape (n_features+1, n_partitions*n_cells) for the linear model
                and (1, n_partitions*n_cells) for the constant model.
        """
        s = jnp.sign(w[:bias_idx])
        thresh = jnp.maximum(jnp.abs(w[:bias_idx]) - self.lam * mu, 0)
        return w.at[:bias_idx].set(s * thresh)


class LaplacianType(Enum):
    """Enum class for the type of Laplacian matrix to use."""

    STANDARD = auto()
    LEFT_NORMALIZED = auto()
    NORMALIZED = auto()


class DistanceWeight(ABC):
    """Base class used for methods that compute distance between data points."""

    def __init__(
        self: DistanceWeight,
        x_train: np.ndarray,
        x_val: np.ndarray | None,
        partitioner: Partitioner,
        **params: dict[str, Any],
    ) -> None:
        """Initializes the distance weight object, for both the training and
        validation data.

        Args:
            x_train (np.ndarray): The features of the training data. Should have
                shape (n_train, n_features).
            x_val (np.ndarray | None): The features of the validation data.
            partitioner (Partitioner): The partitioner object. Used when the
                distance is computed using the tree structure.
        """
        self.train_weights = self.weight(x_train, partitioner, **params)

        if x_val is not None:
            self.val_weights = self.weight(x_val, partitioner, **params)
        else:
            self.val_weights = None

    def __call__(
        self: DistanceWeight,
        is_train: bool,
    ) -> jnp.ndarray:
        """Returns the precomputed weights for either the training or validation
        data.

        Args:
            is_train (bool): Whether to return the training or validation weights.

        Returns:
            jnp.ndarray: The precomputed weights.
        """
        return self.train_weights if is_train else self.val_weights

    @abstractmethod
    def weight(
        self: DistanceWeight,
        x: np.ndarray,
        partitioner: Partitioner,
        **params: dict,
    ) -> np.ndarray:
        """Computes the weights for a given data set.

        Args:
            x (np.ndarray): The feature matrix.
            partitioner (Partitioner): The partitioner object. Used when the
                distance is computed using the tree structure.

        Returns:
            np.ndarray: The computed weights.
        """
        raise NotImplementedError("The weight function is not implemented.")


class RBFWeight(DistanceWeight, ABC):
    """Base class for implementing radial basis function (RBF) weights."""

    def __init__(
        self: RBFWeight,
        x_train: np.ndarray,
        x_val: np.ndarray | None,
        partitioner: Partitioner,
        sigma: float = 1.0,
    ) -> None:
        """Initializes the RBF weight object.

        Args:
            x_train (np.ndarray): The features of the training data.
            x_val (np.ndarray | None): The features of the validation data.
            partitioner (Partitioner): The partitioner object. Used when the
                distance is computed using the tree structure.
            sigma (float, optional): The variance parameter for the RBF kernel.
                Defaults to 1.0.
        """
        assert sigma > 0, "Sigma must be positive."

        self.sigma = sigma

        super().__init__(x_train, x_val, partitioner, sigma=sigma)


class EuclidRBFWeight(RBFWeight, ABC):
    """RBF weights with distance measured by the Euclidean norm."""

    def distance(
        self: EuclidRBFWeight,
        x: np.ndarray,
        partitioner: Partitioner,
    ) -> np.ndarray:
        """Computes the Euclidean distance between data points.

        Args:
            x (np.ndarray): The feature matrix.
            partitioner (Partitioner): The partitioner object. Used when the
                distance is computed using the tree structure. Included for
                interface consistency with the tree-based RBF approaches

        Returns:
            np.ndarray: The computed distance matrix.
        """
        return np.linalg.norm(x[:, None] - x[None, :], axis=-1) ** 2


class TreeRBFWeight(RBFWeight, ABC):
    """RBF weights with distance measured by average path distance between two
    data points for each tree in the partitioner.
    """

    def __init__(
        self: RBFWeight,
        x_train: jnp.ndarray,
        x_val: jnp.ndarray | None,
        partitioner: Partitioner,
        sigma: float = 1,
    ) -> None:
        """Initializes the tree RBF weight object.

        Args:
            x_train (jnp.ndarray): The features of the training data.
            x_val (jnp.ndarray | None): The features of the validation data.
            partitioner (Partitioner): The partitioner object. Used when the
                distance is computed using the tree structure.
            sigma (float, optional): The variance parameter for the RBF kernel.
                Defaults to 1.0.
        """
        assert issubclass(
            type(partitioner), TreePartition
        ), "The partitioner must be a tree partitioner."

        super().__init__(x_train, x_val, partitioner, sigma)

    def distance(
        self: TreeRBFWeight,
        x: np.ndarray,
        partitioner: Partitioner,
    ) -> np.ndarray:
        """Computes the average path distance between two data points for each
        tree in the partitioner.

        Args:
            x (np.ndarray): The feature matrix.
            partitioner (Partitioner): The partitioner object used to compute the
                distance between data points as the average path distance between points in each tree.

        Returns:
            np.ndarray: The computed distance matrix.
        """
        leaf_paths = partitioner.get_leaf_paths(x)

        distances = np.empty((len(leaf_paths), x.shape[0], x.shape[0]))

        for i, path in enumerate(leaf_paths):
            path_sum = path.sum(axis=1).A1  # converts to a dense 1D numpy array
            path_dot_path_T = path.dot(path.T).toarray()

            distance = path_sum[:, None] + path_sum[None, :] - 2 * path_dot_path_T
            distances = distances.at[i].set(distance)

        return distances.mean(axis=0)


class EuclidGaussWeight(EuclidRBFWeight):
    """RBF implemented with Gaussian kernel weights with distance measured by the
    Euclidean norm.
    """

    def weight(
        self: EuclidGaussWeight,
        x: np.ndarray,
        partitioner: Partitioner,
        sigma: float,
    ) -> np.ndarray:
        """Computes the Gaussian kernel weights using the Euclidean distance.

        Args:
            x (np.ndarray): The feature matrix.
            partitioner (Partitioner): The partitioner object. Used when the
                distance is computed using the tree structure. Included for
                interface consistency with the tree-based RBF approaches.
            sigma (float): The variance parameter for the RBF kernel.

        Returns:
            np.ndarray: _description_
        """
        return np.exp(-self.distance(x, partitioner) * sigma)


class TreeGaussWeight(TreeRBFWeight):
    """RBF implemented with Gaussian kernel weights with distance measured by the
    average path distance between data points for each tree in the partitioner.
    """

    def weight(
        self: TreeGaussWeight,
        x: np.ndarray,
        partitioner: Partitioner,
        sigma: float,
    ) -> np.ndarray:
        """Computes the Gaussian kernel weights using the average path distance
        between data points for each tree in the partitioner.

        Args:
            x (np.ndarray): The feature matrix.
            partitioner (Partitioner): The partitioner object. Used to compute the
                distance between data points as the average path distance between points in each tree.
            sigma (float): The variance parameter for the RBF kernel.

        Returns:
            np.ndarray: _description_
        """
        return np.exp(-self.distance(x, partitioner) * sigma)


class EuclidMultiQuadWeight(EuclidRBFWeight):
    """Multiquadric kernel weights with distance measured by the Euclidean norm."""

    def weight(
        self: EuclidMultiQuadWeight,
        x: np.ndarray,
        partitioner: Partitioner,
        sigma: float,
    ) -> np.ndarray:
        """Computes the multiquadric kernel weights using the Euclidean distance.

        Args:
            x (np.ndarray): The feature matrix.
            partitioner (Partitioner): The partitioner object. Used when the
                distance is computed using the tree structure. Included for
                interface consistency with the tree-based MultiQuadratic approaches.
            sigma (float): The variance parameter for the RBF kernel.

        Returns:
            np.ndarray: The computed weights.
        """
        weights = self.distance(x, partitioner)
        mask = weights != 0
        weights = np.divide(1, 1 + weights * sigma, where=mask)
        return weights.at[~mask].set(0)


class TreeMultiQuadWeight(TreeRBFWeight):
    """RBF implemented with multiquadric kernel weights with distance measured by the
    average path distance between data points for each tree in the partitioner.
    """

    def weight(
        self: TreeMultiQuadWeight,
        x: np.ndarray,
        partitioner: Partitioner,
        sigma: float,
    ) -> np.ndarray:
        """Computes the multiquadric kernel weights using the average path distance
        between data points for each tree in the partitioner.

        Args:
            x (np.ndarray): The feature matrix.
            partitioner (Partitioner): The partitioner object. Used to compute the
                distance between data points as the average path distance between
                points in each tree
            sigma (float): The variance parameter for the RBF kernel.

        Returns:
            np.ndarray: The computed weights.
        """
        weights = self.distance(x, partitioner)
        mask = weights != 0
        weights = np.divide(1, 1 + weights * sigma, where=mask)
        return weights.at[~mask].set(0)


class Laplacian(Penalty, ABC):
    """Base class for implementing Laplacian penalties for JOPLEn."""

    def __init__(
        self: Laplacian,
        is_smooth: bool,
        lam: float = 1.0,
        sigma: float = 1.0,
        weight_class: type[DistanceWeight] = EuclidGaussWeight,
        laplacian_type: LaplacianType = LaplacianType.STANDARD,
    ) -> None:
        """Initializes the Laplacian penalty.

        Args:
            is_smooth (bool): Whether the penalty is smooth or not. This is used to
                group the penalty with the gradient or proximal operator weight
                update. It is smooth for penalties like the squared Laplacian and
                nonsmooth for penalties like the total variation.
            lam (float, optional): The regularization parameter. Defaults to 1.0.
            sigma (float, optional): The variance parameter for the RBF kernel.
                Defaults to 1.0.
            weight_class (type[DistanceWeight], optional): The method used to compute
                the distance between data points. Defaults to EuclidGaussWeight.
            laplacian_type (LaplacianType, optional): The type of Laplacian matrix
                to use. Defaults to LaplacianType.STANDARD.
        """
        super().__init__(is_smooth=is_smooth)

        assert lam > 0, "The regularization parameter must be positive."
        assert sigma > 0, "The variance parameter must be positive."

        self.lam = lam
        self.sigma = sigma
        self.laplacian_type = laplacian_type
        self.weight_class = weight_class

    def create_laplacian(self: Laplacian, weights: np.ndarray) -> jnp.ndarray:
        """Creates the Laplacian matrix from the weights. See this link for more
        information: https://en.wikipedia.org/wiki/Laplacian_matrix.

        Args:
            weights (np.ndarray): The distance weights between data points.

        Returns:
            jnp.ndarray: The Laplacian matrix.
        """
        if self.laplacian_type == LaplacianType.LEFT_NORMALIZED:
            s = np.sum(weights, axis=1)
            d_inv = np.reciprocal(s, where=s != 0)
            L = d_inv[:, None] * weights
        elif self.laplacian_type == LaplacianType.NORMALIZED:
            s = np.sqrt(np.sum(weights, axis=1))
            d_inv = np.reciprocal(s, where=s != 0)
            L = d_inv[:, None] * weights * d_inv[None, :]
        elif self.laplacian_type == LaplacianType.STANDARD:
            L = weights
        else:
            raise ValueError(f"Invalid Laplacian type: {self.laplacian_type}")

        return jnp.array(L, dtype=DTYPE)

    def build(
        self: Laplacian,
        x_train: np.ndarray,
        x_val: np.ndarray,
        partitioner: Partitioner,
    ) -> None:
        """Precomputes the Laplacian matrix for the training and validation data.

        Args:
            x_train (np.ndarray): The features of the training data. Should have
                shape (n_train, n_features).
            x_val (np.ndarray): The features of the validation data. Should have
                shape (n_val, n_features).
            partitioner (Partitioner): The partitioner object. Used for Laplacian
                penalties where distance is measured by the tree structure. Included
                for interface consistency with the tree-based approaches.
        """
        self.weight = self.weight_class(x_train, x_val, partitioner, self.sigma)

        self.L_train = self.create_laplacian(self.weight(True))
        self.L_val = self.create_laplacian(self.weight(False))


class SquaredLaplacian(Laplacian):
    """Creates a squared Laplacian penalty."""

    def __init__(
        self: SquaredLaplacian,
        **kwargs: dict,
    ) -> None:
        """Initializes the squared Laplacian penalty."""
        super().__init__(
            is_smooth=True,
            **kwargs,
        )

    def __call__(
        self: SquaredLaplacian,
        w: jnp.ndarray,
        bias_idx: int | None,
        x: jnp.ndarray,
        y_pred: jnp.ndarray,
        s: jnp.ndarray,
        is_train: bool,
    ) -> float:
        """Computes the penalty value using the precomputed Laplacian matrix.

        Args:
            w (jnp.ndarray): The weights of the JOPLEn model.
            bias_idx (int | None): The index of the bias term in the weights.
            x (jnp.ndarray): The features of the data. Should have shape
                (n_data_points, n_features+1) for the linear model and (n_data_points,
                1) for the constant model.
            y_pred (jnp.ndarray): The predicted response values. Sholud have
                shape (n_data_points, 1).
            s (jnp.ndarray): The partition mask for the data. Indicates which
                partition and cell each data point belongs to. Should have shape
                (n_data_points, n_partitions*n_cells).
            is_train (bool): Whether the penalty is being computed for the training
                or validation data. This is used to determine which precomputed
                Laplacian matrix to use: the training or validation Laplacian.

        Returns:
            float: The computed penalty value.
        """
        L = self.L_train if is_train else self.L_val

        return self.lam * float((y_pred.T @ L @ y_pred / (2 * x.shape[0])).flatten()[0])

    def grad(
        self: SquaredLaplacian,
        mu: float,
        w: jnp.ndarray,
        bias_idx: int | None,
        x: jnp.ndarray,
        y_pred: jnp.ndarray,
        s: jnp.ndarray,
        is_train: bool,
    ) -> jnp.ndarray:
        """Computes the gradient of the Laplacian penalty.

        Args:
            mu (float): The step size for the gradient update.
            w (jnp.ndarray): The weights of the JOPLEn model. Should have shape
                (n_features+1, n_partitions*n_cells) for the linear model and
                (1, n_partitions*n_cells) for the constant model.
            bias_idx (int | None): The index of the bias term in the weights.
            x (jnp.ndarray): The features of the data. Should have shape
                (n_data_points, n_features+1) for the linear model and (n_data_points,
                1) for the constant model.
            y_pred (jnp.ndarray): The predicted response values. Should have shape
                (n_data_points, 1).
            s (jnp.ndarray): The partition mask for the data. Indicates which
                partition and cell each data point belongs to. Should have shape
                (n_data_points, n_partitions*n_cells).
            is_train (bool): The penalty is being computed for the training or
                validation data.

        Returns:
            jnp.ndarray: The gradient to be applied to the weights. Should have
            shape (n_features+1, n_partitions*n_cells) for the linear model and
            (1, n_partitions*n_cells) for the constant model.
        """
        L = self.L_train if is_train else self.L_val

        # L may not be symmetric
        res = x.T @ ((L @ y_pred) * s)
        res += x.T @ ((L.T @ y_pred) * s)

        return self.lam * mu * res / (2 * x.shape[0])
