from enum import IntEnum
from typing import Any, Dict, List

import attr
import numpy as np


class Signal(IntEnum):
    NOT = 0
    LONG = 1
    SHORT = -1
    POSITIVE = 2
    NEGATIVE = -2


@attr.s(auto_attribs=True)
class GraphContext:
    price_open: np.ndarray
    price_close: np.ndarray
    price_high: np.ndarray
    price_low: np.ndarray
    tick_volume: np.ndarray


@attr.s(auto_attribs=True)
class CritterRule:
    op: str  # "gt", "lt"...
    ref: Any
    assign: Signal  # "LONG", "SHORT", "POSITIVE", ...
    params: Dict[str, Any] = attr.Factory(dict)


@attr.s(auto_attribs=True)
class Node:
    id: str
    model: str
    critters: List[CritterRule]
    inputs: List[Any] = attr.Factory(list)
    params: Dict[str, Any] = attr.Factory(dict)


@attr.s(auto_attribs=True, frozen=True)
class StrategyOutputKeys:
    buy: str


@attr.s(auto_attribs=True)
class Strategy:
    name: str
    output_keys: StrategyOutputKeys
    nodes: List[Node] = attr.Factory(list)
