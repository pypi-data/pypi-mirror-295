from typing import Any

import numpy as np
from sklearn.base import ClassifierMixin, RegressorMixin
from sklearn.ensemble._base import BaseEnsemble
from sklearn.linear_model._base import LinearClassifierMixin, LinearModel


class FriedmanRefit:
    """Friedman Refit is a method that refits the predictions of an ensemble
    model with a linear model. This is a simpler approach than Global
    Refinement.
    """

    def __init__(
        self,
        base_est_class: type[BaseEnsemble],
        refit_est_class: type[LinearModel],
    ) -> None:
        """Initializes the FriedmanRefit object.

        Args:
            base_est_class (type[BaseEnsemble]): The ensemble model to be refit
            refit_est_class (type[LinearModel]): The model that will be used to
                weight the predictions of the ensemble.
        """
        assert issubclass(
            base_est_class, BaseEnsemble
        ), "base_est_class must be an ensemble"

        is_lin_class = issubclass(refit_est_class, LinearClassifierMixin)
        is_lin_reg = issubclass(refit_est_class, RegressorMixin)
        assert (
            is_lin_class or is_lin_reg
        ), f"refit_est_class must be a linear model, given {refit_est_class}"

        assert issubclass(base_est_class, ClassifierMixin) == issubclass(
            refit_est_class, ClassifierMixin
        ), "base_est_class and refit_est_class must both be classifiers or regressors"

        self.is_classifier = issubclass(base_est_class, ClassifierMixin)

        self.base_est_class: type[BaseEnsemble] = base_est_class
        self.refit_est_class: type[LinearModel] = refit_est_class

    def pred_ind(self, X: np.ndarray) -> np.ndarray:
        """Makes predictions with the base estimator.

        Args:
            X (np.ndarray): The input features, shape (n_samples, n_features)

        Returns:
            np.ndarray: The predictions of the base estimator, shape (n_samples,
                n_estimators)
        """
        # Assuming that there is only one output
        estimators = np.array(self.base_est.estimators_).reshape(-1)

        preds = np.zeros((X.shape[0], len(estimators)))

        for i, est in enumerate(estimators):
            preds[:, i] = est.predict(X)

        return preds

    def fit(
        self,
        X: np.ndarray,
        y: np.ndarray,
        base_params: dict[str, Any] | None = None,
        refit_params: dict[str, Any] | None = None,
    ):
        """Fits the base estimator and the refit estimator.

        Args:
            X (np.ndarray): The input features, shape (n_samples, n_features)
            y (np.ndarray): The response variable, shape (n_samples,)
            base_params (dict[str, Any] | None, optional): parameters for the
                base estimator. Defaults to None.
            refit_params (dict[str, Any] | None, optional): parameters for the
                refit estimator. Defaults to None.
        """
        refit_params = refit_params or {}
        base_params = base_params or {}

        self.base_est: BaseEnsemble = self.base_est_class(**base_params)
        self.refit_est: LinearModel = self.refit_est_class(**refit_params)

        self.base_est.fit(X, y)

        preds = self.pred_ind(X)

        self.refit_est.fit(preds, y)

    def predict(self, X):
        """Make a prediction using the refit estimator.

        Args:
            X (np.ndarary): Input features, shape (n_samples, n_features)

        Returns:
            np.ndarary: The predictions of the refit estimator, shape (n_samples,)
        """
        assert hasattr(self, "base_est"), "You must fit the model first"
        assert hasattr(self, "refit_est"), "You must fit the model first"

        preds = self.pred_ind(X)

        return self.refit_est.predict(preds)

    def predict_proba(self, X):
        """Make a prediction using the refit estimator, assuming that the refit
            estimator is a classifier.

        Args:
            X (np.ndarray): Input features, shape (n_samples, n_features)

        Returns:
            np.ndarray: The predictions of the refit estimator, shape (n_samples,)
        """
        assert hasattr(self, "base_est"), "You must fit the model first"
        assert hasattr(self, "refit_est"), "You must fit the model first"
        assert self.is_classifier, "predict_proba is only available for classifiers"

        preds = self.pred_ind(X)

        if self.is_classifier:
            return self.refit_est.predict_proba(preds)[:, 1]
        else:
            return self.refit_est.predict_proba(preds)


if __name__ == "__main__":
    print("Testing Regression")
    from sklearn.datasets import load_diabetes
    from sklearn.ensemble import GradientBoostingRegressor
    from sklearn.linear_model import Lasso, Ridge
    from sklearn.metrics import root_mean_squared_error
    from sklearn.model_selection import train_test_split

    def rmse(y_true: np.ndarray, y_pred: np.ndarray):
        return root_mean_squared_error(y_true, y_pred)

    diabetes = load_diabetes()
    X, y = diabetes.data, diabetes.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # fr = FriedmanRefit(GradientBoostingRegressor, Ridge)
    # fr.fit(X_train, y_train, refit_params={"alpha": 15.0})
    fr = FriedmanRefit(GradientBoostingRegressor, Lasso)
    fr.fit(X_train, y_train, refit_params={"alpha": 100.0})

    gb = GradientBoostingRegressor()
    gb.fit(X_train, y_train)

    norm_preds = gb.predict(X_test)
    fr_preds = fr.predict(X_test)

    print(f"GBR RMSE: {rmse(y_test, norm_preds)}")
    print(f"FR RMSE: {rmse(y_test, fr_preds)}")

    print("Testing Classification")
    from sklearn.datasets import load_breast_cancer
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score

    cancer = load_breast_cancer()
    X, y = cancer.data, cancer.target

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    fr = FriedmanRefit(GradientBoostingClassifier, LogisticRegression)
    fr.fit(X_train, y_train)

    gb = GradientBoostingClassifier()
    gb.fit(X_train, y_train)

    norm_preds = gb.predict(X_test)
    fr_preds = fr.predict(X_test)

    print(f"GBR Accuracy: {accuracy_score(y_test, norm_preds)}")
    print(f"FR Accuracy: {accuracy_score(y_test, fr_preds)}")
