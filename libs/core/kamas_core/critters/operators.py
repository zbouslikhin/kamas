import numpy as np
from typing import Union

ArrayLike = Union[np.ndarray, float]


def gt(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    return np.greater(a, b)


def lt(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    return np.less(a, b)


def eq(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    return np.equal(a, b)


def and_(*args: ArrayLike) -> np.ndarray:
    """
    Logical AND over any number of boolean arrays or scalars.
    """
    if not args:
        raise ValueError("and_ requires at least one argument")
    result = np.asarray(args[0])
    for arr in args[1:]:
        result = np.logical_and(result, arr)
    return result


def or_(*args):
    if not args:
        raise ValueError("python_or requires at least one argument")

    return np.array(
        [
            next(v for v in values if v) if any(values) else values[-1]
            for values in zip(*args)
        ]
    )


def sub(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    return np.subtract(a, b)


def div(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    return np.divide(a, b)
