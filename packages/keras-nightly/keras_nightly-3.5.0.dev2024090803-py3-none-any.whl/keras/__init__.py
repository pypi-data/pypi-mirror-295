import os

# DO NOT EDIT. Generated by api_gen.sh
from keras.api import DTypePolicy
from keras.api import FloatDTypePolicy
from keras.api import Function
from keras.api import Initializer
from keras.api import Input
from keras.api import InputSpec
from keras.api import KerasTensor
from keras.api import Layer
from keras.api import Loss
from keras.api import Metric
from keras.api import Model
from keras.api import Operation
from keras.api import Optimizer
from keras.api import Quantizer
from keras.api import Regularizer
from keras.api import Sequential
from keras.api import StatelessScope
from keras.api import SymbolicScope
from keras.api import Variable
from keras.api import __version__
from keras.api import activations
from keras.api import applications
from keras.api import backend
from keras.api import callbacks
from keras.api import config
from keras.api import constraints
from keras.api import datasets
from keras.api import device
from keras.api import distribution
from keras.api import dtype_policies
from keras.api import export
from keras.api import initializers
from keras.api import layers
from keras.api import legacy
from keras.api import losses
from keras.api import metrics
from keras.api import mixed_precision
from keras.api import models
from keras.api import name_scope
from keras.api import ops
from keras.api import optimizers
from keras.api import preprocessing
from keras.api import quantizers
from keras.api import random
from keras.api import regularizers
from keras.api import saving
from keras.api import tree
from keras.api import utils
from keras.api import version

# END DO NOT EDIT.

# Add everything in /api/ to the module search path.
__path__.append(os.path.join(os.path.dirname(__file__), "api"))  # noqa: F405

# Don't pollute namespace.
del os


# Never autocomplete `.src` or `.api` on an imported keras object.
def __dir__():
    keys = dict.fromkeys((globals().keys()))
    keys.pop("src")
    keys.pop("api")
    return list(keys)


# Don't import `.src` or `.api` during `from keras import *`.
__all__ = [
    name
    for name in globals().keys()
    if not (name.startswith("_") or name in ("src", "api"))
]
