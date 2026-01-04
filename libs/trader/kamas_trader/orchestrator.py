from kamas_core.interactors.constants import Symbols
from datetime import date, datetime
from typing import Callable, Iterable

import pandas as pd
import numpy as np
from kamas_core.api import StrategyRunResult, run_strategy

from kamas_trader.models import Trade

ExitRule = Callable[[Trade, float], bool]


class TradeManager:
    def __init__(self, exit_rules: Iterable):
        self.exit_rules = exit_rules
        self.current_trade: Trade | None = None

    def check_entry(self, strategy_result: StrategyRunResult, today_unix_date: int):
        signal_map = dict(zip(strategy_result.time, strategy_result.buy_signal))
        return signal_map.get(today_unix_date, False)


class TradeOrchestrator:
    symbols: list[str]
    strategy_name: str
    traders: dict[str, TradeManager] = {}

    def __init__(
        self,
        symbols: list[Symbols],
        strategy_name: str,
    ) -> None:
        self.symbols = symbols
        self.strategy_name = strategy_name
        self.traders: dict[str, TradeManager] = {
            symbol: TradeManager([]) for symbol in symbols
        }

    def on_price_tick(self, start_date: datetime, end_date: datetime):
        for symbol in self.symbols:
            result = run_strategy(symbol, self.strategy_name, start_date, end_date)
            self.traders[symbol].check_entry(result, end_date)

    # def run_daily(self, start_date: datetime):
    #     """
    #     Wrapper to run on_price_tick **once per new day**
    #     """
    #     _last_run_date: date | None = None
    #     today = datetime.now().date()
    #     if _last_run_date != today:
    #         _last_run_date = today
    #         end_date = datetime.now()
    #         self.on_price_tick(start_date, end_date)

    def _run_for_date(self, start_date: datetime, current_date: datetime):
        """
        Run strategy and trade checks for a single date (end-of-day simulation)
        """
        if (current_date - start_date).days <= 2:
            return

        for symbol in self.symbols:
            result = run_strategy(symbol, self.strategy_name, start_date, current_date)
            today_date_unix = int(
                current_date.replace(hour=0, minute=0, second=0).timestamp()
            )
            if self.traders[symbol].check_entry(
                result,
                today_date_unix,
            ):
                print("is entry")
                print(today_date_unix)
