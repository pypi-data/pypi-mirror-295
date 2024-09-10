from enum import Enum, auto
import jax.numpy as jnp

DTYPE = jnp.float32


class LossType(Enum):
    """The type of task performed by the model. Loss functions perform these
    predictions, so they need to know the type of task.
    """

    multinomial_classification = auto()
    binary_classification = auto()
    regression = auto()
    ranking = auto()


class CellModel(Enum):
    """What function to use in each cell."""

    constant = auto()
    linear = auto()


class NormType(Enum):
    """The norm that should be used for multitask JOPLEn."""

    L21 = auto()
    LINF1 = auto()
