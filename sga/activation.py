import math


def identity(x):
    return x


def heaviside(x):
    return 1 if x >= 0 else 0


def sigmoid(x):
    return 1 / (1 + math.exp(x))


def tanh(x):
    return math.tanh(x)


def atan(x):
    return math.atan(x)


def relu(x):
    return max(x, 0)


def softplus(x):
    return math.log(1 + math.exp(x), math.e)


def sin(x):
    return math.sin(x)


def gauss(x):
    return math.exp(-x**2)
