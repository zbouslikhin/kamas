import attr
import numpy as np

@attr.s(auto_attribs=True)
class GraphContext:
    close: np.ndarray
    high: np.ndarray
    low: np.ndarray
    tick_volume: np.ndarray
