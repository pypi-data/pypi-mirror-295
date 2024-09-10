import numpy as np
import pytest
from sklearn.datasets import make_classification, make_regression

from JOPLEn.enums import CellModel, LossType, NormType
from JOPLEn.multitask import MTJOPLEn
from JOPLEn.partitioner import (
    CBPartition,
    ExtraTreePartition,
    GBPartition,
    LGBMPartition,
    LinearForestPartition,
    RFPartition,
    VPartition,
)
from JOPLEn.singletask import JOPLEn
from JOPLEn.st_loss import LogisticLoss, SquaredError
from JOPLEn.st_penalty import (
    Group21Norm,
    GroupInf1Norm,
    L1Norm,
    NuclearNorm,
    SquaredFNorm,
)


def make_multitask_classification(
    n_samples=100,
    n_features=20,
    n_classes=3,
    n_tasks=2,
    n_informative=2,
    n_redundant=2,
    random_state=None,
):

    # Generate the base dataset for one task
    X, y_base = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_classes=n_classes,
        n_informative=n_informative,
        n_redundant=n_redundant,
        random_state=random_state,
    )

    # Initialize the multitask labels array
    Y = np.zeros((n_samples, n_tasks), dtype=int)

    # Copy the base task labels to each task
    for task in range(n_tasks):
        Y[:, task] = y_base

    # Optionally introduce some variability in tasks
    if n_tasks > 1:
        rng = np.random.default_rng(random_state)
        for task in range(n_tasks):
            noise = rng.integers(low=0, high=n_classes, size=n_samples)
            Y[:, task] = (Y[:, task] + noise) % n_classes

    return X, Y


def gen_train_data(is_classification, is_multitask):
    from sklearn.model_selection import train_test_split

    kwargs = {
        "n_samples": 1000,
        "n_features": 20,
        "n_informative": 10,
        "random_state": 0,
    }

    if is_classification:
        if is_multitask:
            x, y = make_multitask_classification(**kwargs, n_classes=3, n_tasks=2)
        else:
            x, y = make_classification(**kwargs, n_classes=2)
            y = y.flatten()
    else:
        x, y = make_regression(**kwargs, n_targets=2 if is_multitask else 1, noise=0.1)

    # Split the dataset into training and test sets
    if is_multitask:
        idx = np.arange(x.shape[0])
        idx_train, idx_val = train_test_split(idx, test_size=0.2, random_state=0)
        y = y.T
        x = x[None, :].repeat(y.shape[0], axis=0)
        x_train, x_val = x[:, idx_train], x[:, idx_val]
        y_train, y_val = y[:, idx_train], y[:, idx_val]
    else:
        x_train, x_val, y_train, y_val = train_test_split(
            x, y, test_size=0.2, random_state=0
        )

    return x_train, y_train, x_val, y_val


# Just makes sure that the model runs without any errors
@pytest.mark.parametrize(
    "part",
    [
        VPartition,
        ExtraTreePartition,
        LGBMPartition,
        CBPartition,
        RFPartition,
        GBPartition,
        LinearForestPartition,
    ],
)
@pytest.mark.parametrize("loss_fn", [SquaredError, LogisticLoss])
@pytest.mark.parametrize("cell_model", [CellModel.linear, CellModel.constant])
@pytest.mark.parametrize(
    "reg",
    [
        SquaredFNorm,
        Group21Norm,
        GroupInf1Norm,
        NuclearNorm,
        L1Norm,
    ],
)
def test_st_reg(part, loss_fn, cell_model, reg) -> None:
    x_train, y_train, x_val, y_val = gen_train_data(
        is_classification=(loss_fn().loss_type == LossType.binary_classification),
        is_multitask=False,
    )

    jp = JOPLEn(
        partitioner=part,
        n_cells=8,
        n_partitions=5,
        loss_fn=loss_fn,
        cell_model=cell_model,
        mu=1e-3,
        max_iters=10,
        early_stop=False,
        rescale=False,
        regularizers=[reg(lam=0.01)],
    )

    jp.fit(
        x_train,
        y_train,
        val_x=x_val,
        val_y=y_val,
        print_epochs=10,
    )


# Just makes sure that the model runs without any errors
@pytest.mark.parametrize(
    "part",
    [
        VPartition,
        ExtraTreePartition,
        LGBMPartition,
        CBPartition,
        RFPartition,
        GBPartition,
        LinearForestPartition,
    ],
)
@pytest.mark.parametrize("loss_fn", [SquaredError, LogisticLoss])
@pytest.mark.parametrize("core_lam", [0.0, 0.1])
@pytest.mark.parametrize("task_lam", [0.0, 0.1])
@pytest.mark.parametrize("core_alpha", [0.0, 0.1])
@pytest.mark.parametrize("task_alpha", [0.0, 0.1])
@pytest.mark.parametrize("norm_type", [NormType.LINF1, NormType.L21])
@pytest.mark.parametrize("rel_lr", [None, [1, 2]])
def test_mt_reg(
    part, loss_fn, core_lam, task_lam, core_alpha, task_alpha, norm_type, rel_lr
):
    x_train, y_train, x_val, y_val = gen_train_data(
        is_classification=(loss_fn().loss_type == LossType.binary_classification),
        is_multitask=True,
    )

    mtjp = MTJOPLEn(
        partitioner=part,
        n_cells=8,
        n_partitions=5,
        random_state=0,
    )

    mtjp.fit(
        x_train,
        y_train,
        lst_val_x=x_val,
        lst_val_y=y_val,
        core_lam=core_lam,
        task_lam=task_lam,
        core_alpha=core_alpha,
        task_alpha=task_alpha,
        norm_type=norm_type,
        verbose=False,
        rel_lr=rel_lr,
        max_iters=10,
    )
