from __future__ import annotations

import warnings
from abc import ABC, abstractmethod
from typing import Any, Union

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from catboost import CatBoostClassifier, CatBoostRegressor, Pool
from lightgbm import LGBMClassifier, LGBMRegressor
from lineartree import LinearForestClassifier, LinearForestRegressor
from numpy.random import RandomState
from scipy.spatial import Voronoi, voronoi_plot_2d
from sklearn.ensemble import (
    ExtraTreesClassifier,
    ExtraTreesRegressor,
    GradientBoostingClassifier,
    GradientBoostingRegressor,
    RandomForestClassifier,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import pairwise_distances_argmin_min
from xgboost import DMatrix, XGBClassifier, XGBRegressor

from .enums import LossType


def numpify(x: np.ndarray | pd.DataFrame | pd.Series) -> np.ndarray:
    """Convert a pandas DataFrame to a numpy array if necessary.

    Args:
        x (pd.DataFrame | np.ndarray): The input data. Should have shape (n_samples, n_features).

    Returns:
        np.ndarray: The input data as a numpy array. Should have shape (n_samples, n_features).
    """
    if isinstance(x, pd.DataFrame) or isinstance(x, pd.Series):
        x = x.to_numpy()

    if len(x.shape) == 1:
        x = x.reshape(-1, 1)

    return x


class Partitioner(ABC):
    """A class for splitting the feature space into partitions and cells, which
    can then be used in the JOPLEn algorithm.
    """

    def __init__(
        self: Partitioner,
        n_cells: int,
        n_partitions: int,
        loss_type: LossType,
        random_state: Union[int, RandomState],
        keep_int: bool = False,
        **model_kwargs: dict[str, Any],
    ) -> None:
        """Initializes a Partitioner object.

        Args:
            self (Partitioner): The partitioner object.
            n_cells (int): How many cells should be in each partition.
            n_partitions (int): How many partitions to create.
            loss_type (LossType): Whether the loss is regression or classification.
            random_state (Union[int, RandomState]): The random state to use when
                constructing the partitions.
            keep_int (bool, optional): For some reason, CatBoost only accepts
                integer random states, not actual RandomState objects. Defaults
                to False.
        """
        # keep_int is necessary for CatBoost for some reason
        self.n_cells: int = n_cells
        self.n_partitions: int = n_partitions
        self.loss_type: LossType = loss_type
        self.model_kwargs: dict[str, Any] = model_kwargs

        if not isinstance(random_state, RandomState) and not keep_int:
            self.state: RandomState | int = RandomState(random_state)
        else:
            self.state: RandomState | int = random_state

    @abstractmethod
    def partition(self: Partitioner, x: np.ndarray) -> np.ndarray:
        """Take input data and apply a partition mask to it.

        Args:
            self (Partitioner): The partitioner object.
            x (np.ndarray): The input data to be partitioned. Should have shape (n_samples, n_features).

        Returns:
            np.ndarray: The partitioned data.
        """


class VPartition(Partitioner):
    def __init__(
        self: VPartition,
        x: np.ndarray,
        y: np.ndarray,
        n_cells: int,
        n_partitions: int,
        loss_type: LossType,
        random_state: int = 0,
        x_val: np.ndarray | None = None,
        y_val: np.ndarray | None = None,
        **model_kwargs: dict[str, Any],
    ) -> None:
        """Initializes a VPartition object.

        Args:
            x (np.ndarray): Array of shape (n_samples, n_features) containing the
                input data.
            y (np.ndarray): Array of shape (n_samples,) containing the target
                response variables.
            n_cells (int): Number of Voronoi cells to create.
            n_partitions (int): Number of partitions to create.
            random_state (int, optional): Seed for the random number generator.
                Defaults to 0.
        """
        super().__init__(n_cells, n_partitions, loss_type, random_state, **model_kwargs)

        self._create_voronoi(x)

    def _create_voronoi(self: VPartition, x: np.ndarray) -> None:
        idx = self.state.randint(0, x.shape[0], size=(self.n_cells, self.n_partitions))

        self.vor_points = x[idx]

    def partition(self: VPartition, x: np.ndarray) -> np.ndarray:
        """Partition the input data using Voronoi cells.

        Args:
            self (VPartition): The Voronoi partitioner object.
            x (np.ndarray): The input data to be partitioned.

        Returns:
            np.ndarray: The partitioned data wth shape (n_samples, n_partitions)
        """
        # Check if the dimensions are compatible
        if x.shape[1] != self.vor_points.shape[2]:
            msg = (
                "Dimension mismatch between input data and Voronoi points:"
                f"{x.shape[1]}, {self.vor_points.shape[2]}"
            )
            raise ValueError(msg)

        x = numpify(x)

        # Initialize an empty list to store the results
        concatenated_indices = []

        # Iterate through the n different sets of Voronoi points
        for i in range(self.vor_points.shape[1]):
            vor_points_i = self.vor_points[:, i, :]
            indices, _ = pairwise_distances_argmin_min(x, vor_points_i)
            concatenated_indices.append(indices.reshape(-1, 1))

        # Concatenate the results along the specified axis
        return np.hstack(concatenated_indices)

    def plot_partitions(self: VPartition, max_to_plot: int = 1, ax=None) -> None:
        """Plot the Voronoi partitions. This is used more for debugging purposes
            than anything else.

        Args:
            self (VPartition): The Voronoi partitioner object.
            max_to_plot (int, optional): The number of partitions to plot.
                Defaults to 1.
            ax (_type_, optional): The matplotlib axis to plot on. Defaults to None.

        """
        from matplotlib import cm

        if ax is None:
            fig, ax = plt.subplots()

        colors = cm.get_cmap("tab10").colors

        for i in range(max_to_plot):
            vor = Voronoi(self.vor_points[:, i, :])
            voronoi_plot_2d(
                vor,
                show_vertices=False,
                line_colors=colors[i],
                line_styles="-",
                point_size=0,
                ax=ax,
            )


class TreePartition(Partitioner, ABC):
    def __init__(
        self,
        x: np.ndarray,
        y: np.ndarray,
        n_cells: int,
        n_partitions: int,
        loss_type: LossType,
        random_state: int = 0,
        prefit_model: Any | None = None,
        x_val: np.ndarray | None = None,
        y_val: np.ndarray | None = None,
        keep_int: bool = False,
        **model_kwargs: dict[str, Any],
    ) -> None:
        """Initializes a TreePartition object.

        Args:
            x (np.ndarray): The input features, an array of shape (n_samples, n_features).
            y (np.ndarray): The target response variables, an array of shape (n_samples,).
            n_cells (int): The number of cells to create in each partition.
            n_partitions (int): The number of partitions to create.
            loss_type (LossType): Whether the loss is regression or classification.
            random_state (int, optional): The random state used by the underlying model. Defaults to 0.
            prefit_model (Any | None, optional): A model which has already been
                fit, and will not be trained again. Defaults to None.
            x_val (np.ndarray | None, optional): The validation features, an
                array of (n_samples, n_features). Defaults to None.
            y_val (np.ndarray | None, optional): The validation response
                variables, an array of (n_samples,). Defaults to None. Defaults to
                None.
            keep_int (bool, optional): Whether to keep the random state as an
                integer or convert it to a RandomState object. Necessary because
                of CatBoost. Defaults to False.
        """
        super().__init__(
            n_cells,
            n_partitions,
            loss_type,
            random_state,
            keep_int,
            **model_kwargs,
        )

        if prefit_model is None:
            self._fit_model(x, y, x_val, y_val)
        else:
            self._prefit_model(prefit_model, x)

        # should provide all of the leaf indices
        train_leaf_indices = self._get_leaves(x)

        assert len(train_leaf_indices.shape) == 2, "Leaf indices must be 2D"

    def partition(self, x: np.ndarray) -> np.ndarray:
        """Create a partition mask for the input data.

        Args:
            x (np.ndarray): The input data to be partitioned, an array of shape (n_samples, n_features).

        Returns:
            np.ndarray: An array of shape (n_samples, n_partitions*n_cells)
                containing the cell index that contains each data point.
        """
        leaf_indices = self._get_leaves(x)
        # Leaf indices are the partitions
        return leaf_indices.astype(int)

    @abstractmethod
    def _get_leaves(self, x: np.ndarray) -> np.ndarray:
        """Get the leaf indices for each data point in each tree. This is unique
            to each model.

        Args:
            x (np.ndarray): The input data, an array of shape (n_samples, n_features).
        """

    @abstractmethod
    def _fit_model(
        self,
        x: np.ndarray,
        y: np.ndarray,
        x_val: np.ndarray,
        y_val: np.ndarray,
    ):
        """Fit the underlying model to the data. This is unique to each model.

        Args:
            x (np.ndarray): The input features, an array of shape (n_samples,
                n_features).
            y (np.ndarray): The target response variables, an array of shape
                (n_samples,).
            x_val (np.ndarray): The validation features, an array of shape
                (n_samples, n_features).
            y_val (np.ndarray): The validation response variables, an array of
                shape (n_samples,).
        """

    @abstractmethod
    def _prefit_model(self, model: Any, x: np.ndarray) -> None:
        """Use a prefit model instead of fitting a new one.

        Args:
            model (Any): The prefit model.
            x (np.ndarray): The input features, an array of shape (n_samples,
                n_features).
        """


class SKLTreePartition(TreePartition):
    """A class for partitioning the feature space using an ensemble of tree-based
    models from scikit-learn.
    """

    def _truncate_classification(self, leaf_indices: np.ndarray) -> np.ndarray:
        """In SKLearn, leaf indices return 3d arrays for classification, but we
            only care about the first two columns. See this link for more details.
            https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingClassifier.html#sklearn.ensemble.GradientBoostingClassifier.apply.

        Args:
            leaf_indices (np.ndarray): The leaf indices for each data point in
                each tree. It has shape (n_samples, n_partitions, n_classes)
                for classification and (n_samples, n_partitions) for regression.

        Returns:
            np.ndarray: The truncated leaf indices, an array of shape (n_samples,
            n_partitions), where each value is the cell index for a given
            partition.
        """
        if len(leaf_indices.shape) == 2:
            return leaf_indices

        return leaf_indices[:, :, 0]

    def _get_leaves(self, x: np.ndarray) -> np.ndarray:
        """Get the leaf indices for each data point in each tree.

        Args:
            x (np.ndarray): The input data, an array of shape (n_samples,
                n_features).

        Returns:
            np.ndarray: The leaf indices for each data point in each tree, an
                array of shape (n_samples, n_partitions), where each value is
                the cell index for a given partition.
        """
        # SKLearn uses the convention that leaf indices start at 1
        leaf_indices = self._truncate_classification(self.model.apply(x))

        # actually rename the leaf indices
        for i in range(leaf_indices.shape[0]):
            for j in range(leaf_indices.shape[1]):
                leaf_indices[i, j] = self.renamer[j][leaf_indices[i, j]]

        return leaf_indices

    def get_leaf_paths(self, x: np.ndarray) -> list[np.ndarray]:
        """Get the decision paths for each data point in each tree. This is
            necessary for the tree-based Laplacian smoothing penalties
            TreeRBFWeight and TreeGaussWeight.

        Args:
            x (np.ndarray): The input data, an array of shape (n_samples, n_features).

        Returns:
            list[np.ndarray]: A list of arrays, where each array contains the
                decision path for a given data point in a given tree.
        """
        decision_paths = []

        for tree in self.model.estimators_[:, 0]:
            decision_paths.append(tree.decision_path(x))

        return decision_paths

    def _fit_model(
        self,
        x: np.ndarray,
        y: np.ndarray,
        x_val: np.ndarray,
        y_val: np.ndarray,
    ):
        """Fit the underlying model to the data. Note that this model does not use
            validation data, but that it accepts them to keep the interface consistent.

        Args:
            x (np.ndarray): The input features, an array of shape (n_samples,
                n_features).
            y (np.ndarray): The target response variables, an array of shape
                (n_samples,).
            x_val (np.ndarray): The validation features, an array of shape
                (n_samples, n_features).
            y_val (np.ndarray): The validation response variables, an array of
                shape (n_samples,).
        """
        match self.loss_type:
            case LossType.regression:
                model_class = self.get_regression_model()
            case LossType.binary_classification | LossType.multinomial_classification:
                model_class = self.get_classification_model()
            case _:
                raise ValueError("Loss type not supported")

        self.model = model_class(  # type: ignore[reportOptionalCall]
            n_estimators=self.n_partitions,
            max_leaf_nodes=self.n_cells,
            random_state=self.state,
            **self.model_kwargs,
        )

        self.model.fit(x, y.flatten())

        self._init_leaf_renamer(x)

    def _init_leaf_renamer(self, x: np.ndarray) -> None:
        """Initialize the leaf renamer, which is used to map leaf indices to cell
            indices. This is necessary because leaf indices are not sequential.

        Args:
            x (np.ndarray): The input data, an array of shape (n_samples,
                n_features).
        """
        # Need to use this really hacky method because leaf indices are not
        # sequential

        # Get leaf indices for each data point in each tree
        # SKLearn uses the convention that leaf indices start at 1
        leaf_indices = self._truncate_classification(self.model.apply(x))

        self.renamer = []

        for tree_leaves in leaf_indices.T:
            d = {v: i for i, v in enumerate(np.unique(tree_leaves))}
            self.renamer.append(d)

    def _prefit_model(self, model: Any, x: np.ndarray) -> None:
        """Use a prefit model instead of fitting a new one.

        Args:
            model (Any): The prefit model.
            x (np.ndarray): An array of shape (n_samples, n_features) containing
                the input data.
        """
        self.model = model

        self._init_leaf_renamer(x)

    @abstractmethod
    def get_regression_model(self):
        """Get the regression model to use for this partitioner. This is defined
        in each subclass.
        """

    @abstractmethod
    def get_classification_model(self):
        """Get the classification model to use for this partitioner. This is
        defined in each subclass.
        """


class ExtraTreePartition(SKLTreePartition):
    """A class for partitioning the feature space using an ensemble of Extra
    Trees models.
    """

    def __init__(
        self,
        x: np.ndarray,
        y: np.ndarray,
        n_cells: int,
        n_partitions: int,
        loss_type: LossType,
        random_state: int = 0,
        prefit_model: Any | None = None,
        x_val: np.ndarray | None = None,
        y_val: np.ndarray | None = None,
        **model_kwargs: dict[str, Any],
    ) -> None:
        """Initializes an ExtraTreePartition object. Uses one random feature
        per split, which is different than the original paper.

        Args:
            x (np.ndarray): The input features, an array of shape (n_samples, n_features).
            y (np.ndarray): The target response variables, an array of shape (n_samples,).
            n_cells (int): The number of cells to create in each partition.
            n_partitions (int): The number of partitions to create.
            loss_type (LossType): Whether the loss is regression or classification.
            random_state (int, optional): The random state used by the underlying model. Defaults to 0.
            prefit_model (Any | None, optional): A model which has already been
                fit, and will not be trained again. Defaults to None.
            x_val (np.ndarray | None, optional): The validation features, an
                array of (n_samples, n_features). Defaults to None.
            y_val (np.ndarray | None, optional): The validation response
                variables, an array of (n_samples,). Defaults to None. Defaults to
                None.
        """
        super().__init__(
            x,
            y,
            n_cells,
            n_partitions,
            loss_type,
            random_state,
            prefit_model,
            x_val,
            y_val,
            max_features=1,
            **model_kwargs,
        )

    def get_regression_model(self):
        return ExtraTreesRegressor

    def get_classification_model(self):
        return ExtraTreesClassifier


class LGBMPartition(TreePartition):
    """Partition the feature space using Light Gradient Boosted Machine (LightGBM)."""

    def _get_leaves(self, x: np.ndarray) -> np.ndarray:
        return self.model.predict(x, pred_leaf=True)

    def _fit_model(
        self,
        x: np.ndarray,
        y: np.ndarray,
        x_val: np.ndarray,
        y_val: np.ndarray,
    ):
        match self.loss_type:
            case LossType.regression:
                model_class = LGBMRegressor
            case LossType.binary_classification | LossType.multinomial_classification:
                model_class = LGBMClassifier
            case _:
                raise ValueError("Loss type not supported")

        self.model = model_class(
            n_estimators=self.n_partitions,
            num_leaves=self.n_cells,
            random_state=self.state,
            verbose=-1,
        )

        if x_val is None or y_val is None:
            eval_set = None
        else:
            eval_set = (x_val, y_val.flatten())

        self.model.fit(x, y.flatten(), eval_set=eval_set)

    def _prefit_model(self, model: Any, x: np.ndarray) -> None:
        self.model = model

    def get_leaf_paths(self, x: np.ndarray) -> list[np.ndarray]:
        raise NotImplementedError("Leaf paths not implemented for LightGBM")


class CBPartition(TreePartition):
    """Partition the feature space using CatBoost."""

    def __init__(
        self,
        x: np.ndarray,
        y: np.ndarray,
        n_cells: int,
        n_partitions: int,
        loss_type: LossType,
        random_state: int = 0,
        prefit_model: Any | None = None,
        x_val: np.ndarray | None = None,
        y_val: np.ndarray | None = None,
        **model_kwargs: dict[str, Any],
    ) -> None:
        super().__init__(
            x,
            y,
            n_cells,
            n_partitions,
            loss_type,
            random_state,
            prefit_model,
            x_val,
            y_val,
            keep_int=True,
            **model_kwargs,
        )

    def _get_leaves(self, x: np.ndarray) -> np.ndarray:
        return self.model.calc_leaf_indexes(x)

    def _fit_model(
        self,
        x: np.ndarray,
        y: np.ndarray,
        x_val: np.ndarray,
        y_val: np.ndarray,
    ):
        match self.loss_type:
            case LossType.regression:
                model_class = CatBoostRegressor
            case LossType.binary_classification | LossType.multinomial_classification:
                model_class = CatBoostClassifier
            case _:
                raise ValueError("Loss type not supported")

        train_pool = Pool(
            x,
            y.flatten(),
            cat_features=self.model_kwargs.get("cat_features"),
        )

        if x_val is None or y_val is None:
            val_pool = None
        else:
            val_pool = Pool(x_val, y_val.flatten())

        max_depth = np.log2(self.n_cells)
        assert max_depth % 1 == 0, "n_cells must be a power of 2"

        self.model = model_class(
            max_depth=int(max_depth),
            iterations=self.n_partitions,
            random_state=self.state,
            allow_writing_files=False,
            **self.model_kwargs,
        )

        self.model.fit(
            train_pool,
            eval_set=val_pool,
            verbose=False,
        )

        self.n_partitions = self.model.tree_count_

    def _prefit_model(self, model: Any, x: np.ndarray) -> None:
        self.model = model

    def get_leaf_paths(self, x: np.ndarray) -> list[np.ndarray]:
        raise NotImplementedError("Leaf paths not implemented for CatBoost")


class RFPartition(SKLTreePartition):
    """Partition the feature space using Random Forest."""

    def get_regression_model(self):
        return RandomForestRegressor

    def get_classification_model(self):
        return RandomForestClassifier


class GBPartition(SKLTreePartition):
    """Partition the feature space using Gradient Boosting."""

    def get_regression_model(self):
        return GradientBoostingRegressor

    def get_classification_model(self):
        return GradientBoostingClassifier


class LinearForestPartition(SKLTreePartition):
    """Partition the feature space using LinearForest, a tree-based model that
    fits linear models to the leaves of each tree in a random forest framework.
    """

    def __init__(
        self,
        x: np.ndarray,
        y: np.ndarray,
        n_cells: int,
        n_partitions: int,
        loss_type: LossType,
        random_state: int = 0,
        prefit_model: Any | None = None,
        x_val: np.ndarray | None = None,
        y_val: np.ndarray | None = None,
        **model_kwargs: dict[str, Any],
    ) -> None:
        super().__init__(
            x,
            y,
            n_cells,
            n_partitions,
            loss_type,
            random_state,
            prefit_model,
            x_val,
            y_val,
            max_features="sqrt",
            **model_kwargs,
        )

    def _fit_model(
        self,
        x: np.ndarray,
        y: np.ndarray,
        x_val: np.ndarray,
        y_val: np.ndarray,
    ):
        assert (np.log2(self.n_cells) % 1) == 0, "n_cells must be a power of 2"

        if "base_estimator" not in self.model_kwargs:
            self.model_kwargs["base_estimator"] = LinearRegression()

        super()._fit_model(x, y, x_val, y_val)

    def get_regression_model(self):
        return LinearForestRegressor

    def get_classification_model(self):
        return LinearForestClassifier
