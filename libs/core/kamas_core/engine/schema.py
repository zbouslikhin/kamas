from typing import List, Any, Optional, Dict
from enum import IntEnum

import numpy as np
import attr


class Signal(IntEnum):
    NOT = 0
    LONG = 1
    SHORT = -1
    POSITIVE = 2
    NEGATIVE = -2

@attr.s(auto_attribs=True)
class GraphContext:
    price_close: np.ndarray
    price_high: np.ndarray
    price_low: np.ndarray
    tick_volume: np.ndarray


@attr.s(auto_attribs=True)
class CritterRule:
    critter: str           # "gt", "lt", etc.
    assign: Signal            # "LONG", "SHORT", "POSITIVE", ...
    params: Dict[str, Any] = attr.Factory(dict)


@attr.s(auto_attribs=True)
class Node:
    id: str
    inputs: List[Any] = attr.Factory(list)
    params: Dict[str, Any] = attr.Factory(dict)
    critters: List[CritterRule]


@attr.s(auto_attribs=True, frozen=True)
class StrategyOutputKeys:
    buy: str


@attr.s(auto_attribs=True)
class Strategy:
    name: str
    output_keys: StrategyOutputKeys
    nodes: List[Node] = attr.Factory(list)
