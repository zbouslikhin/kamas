import numpy as np
from typing import Union

ArrayLike = Union[np.ndarray, float]

def gt(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    return np.greater(a, b)

def lt(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    return np.less(a, b)

def and_(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.logical_and(a, b)

def or_(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    return np.logical_or(a, b)

def sub(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    return np.subtract(a, b)

def div(a: ArrayLike, b: ArrayLike) -> np.ndarray:
    return np.divide(a, b)
