from datetime import datetime
from typing import Dict

import attr
import numpy as np
from numpy.typing import NDArray

from kamas_core.engine.graph import build_graph
from kamas_core.engine.loader import load_strategy
from kamas_core.engine.schema import GraphContext
from kamas_core.helpers import get_rates


@attr.s(auto_attribs=True, frozen=True)
class StrategyRunResult:
    symbol: str
    time: NDArray[np.datetime64]
    price_open: np.ndarray
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
    symbol: str, strategy_name: str, start: datetime, end: datetime
) -> StrategyRunResult:
    """
    Runs a strategy graph on market data and returns computed buy/sell signals.

    Returns a dictionary:
        - 'buy_signal': numpy array
        - 'sell_signal': numpy array
        - 'all_outputs': dict of all intermediate node outputs
    """

    # --- Fetch market data ---
    try:
        rates = get_rates(symbol, start, end)
        ctx = GraphContext(
            price_open=rates["open"].to_numpy(),
            price_close=rates["close"].to_numpy(),
            price_high=rates["high"].to_numpy(),
            price_low=rates["low"].to_numpy(),
            tick_volume=rates["tick_volume"].to_numpy(),
        )

        # --- Load & build strategy ---
        strategy = load_strategy(strategy_name)
        graph = build_graph(strategy)

        # --- Run the strategy graph ---
        outputs = graph.run(ctx)

        return StrategyRunResult(
            symbol=symbol,
            time=rates["time"].to_numpy(),
            price_open=ctx.price_open,
            price_close=ctx.price_close,
            price_high=ctx.price_high,
            price_low=ctx.price_low,
            tick_volume=ctx.tick_volume,
            buy_node_key=strategy.output_keys.buy,
            nodes=outputs,
        )
    except Exception as e:
        raise Exception(f"Here {e}")
