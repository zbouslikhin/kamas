
from datetime import datetime
from typing import Any, Dict

import numpy as np
import attr

from kamas_core.helpers import get_rates
from kamas_core.engine.schema import GraphContext
from kamas_core.engine.loader import load_strategy
from kamas_core.engine.graph import build_graph


@attr.s(auto_attribs=True, frozen=True)
class StrategyRunResult:
    price_close: np.ndarray
    price_high: np.ndarray
    price_low: np.ndarray
    tick_volume: np.ndarray

    buy_node_key: str

    nodes: Dict[str, np.ndarray]

    @property
    def buy_signal(self) -> np.ndarray:
        return self.nodes[self.buy_node_key]
    

def run_strategy(
    symbol: str,
    strategy_name: str,
    start: datetime,
    end: datetime
) -> StrategyRunResult:
    """
    Runs a strategy graph on market data and returns computed buy/sell signals.

    Returns a dictionary:
        - 'buy_signal': numpy array
        - 'sell_signal': numpy array
        - 'all_outputs': dict of all intermediate node outputs
    """

    # --- Fetch market data ---
    rates = get_rates(symbol, start, end)
    ctx = GraphContext(
        price_close=rates["close"],
        price_high=rates["high"],
        price_low=rates["low"],
        tick_volume=rates["tick_volume"]
    )

    # --- Load & build strategy ---
    strategy = load_strategy(strategy_name)
    graph = build_graph(strategy)

    # --- Run the strategy graph ---
    outputs = graph.run(ctx)

    return StrategyRunResult(
        price_close=ctx.price_close,
        price_high=ctx.price_high,
        price_low=ctx.price_low,
        tick_volume=ctx.tick_volume,
        buy_node_key=strategy.output_keys.buy,
        nodes=outputs,
    )