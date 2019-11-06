import math
from typing import Callable


def identity(x):
    return x


def heaviside(x):
    return 1 if x >= 0 else 0


def sigmoid(x):
    return 1 / (1 + math.exp(x))


def relu(x):
    return max(x, 0)


def softplus(x):
    return math.log(1 + math.exp(x), math.e)


def gauss(x):
    return math.exp(-x**2)


def get_function(function: str) -> Callable:
    if function == "identity":
        return identity
    if function == "heaviside":
        return heaviside
    if function == "sigmoid":
        return sigmoid
    if function == "tanh":
        return math.tanh
    if function == "arctan" or function == "atan":
        return math.atan
    if function == "relu":
        return relu
    if function == "softplus":
        return softplus
    if function == "sin":
        return math.sin
    if function == "gauss":
        return gauss
    print("Selected activation function does not exist; identity selected by default")
    return identity
