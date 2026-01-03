import datetime
from typing import Iterable, Callable, Generator
import numpy as np

from kamas_trader.models import Trade
from kamas_trader.events import TradeEvent

ExitRule = Callable[[Trade, float], bool]


def trade_generator(
    prices: np.ndarray,
    times: np.ndarray,
    buy_signal: np.ndarray,
    exit_rules: Iterable[ExitRule],
) -> Generator[TradeEvent, None, None]:
    trade: Trade | None = None

    for i in range(len(prices)):
        price = prices[i]
        time = times[i]

        # --- ENTRY ---
        if buy_signal[i] and trade is None:
            trade = Trade(
                entry_price=price,
                entry_time=time,
                entry_index=i,
            )
            yield TradeEvent("entry", i, time, price)
            continue

        # --- EXIT ---
        if trade is not None:
            for rule in exit_rules:
                if rule(trade, price):
                    trade.exit_price = price
                    trade.exit_time = time
                    trade.exit_index = i
                    yield TradeEvent("exit", i, time, price)
                    trade = None
                    break
