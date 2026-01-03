from datetime import date, datetime
from typing import Callable, Iterable

import numpy as np
from kamas_core.api import StrategyRunResult, run_strategy

from kamas_trader.models import Trade

ExitRule = Callable[[Trade, float], bool]


class TradeManager:
    def __init__(self, exit_rules: Iterable):
        self.exit_rules = exit_rules
        self.current_trade: Trade | None = None

    def check_entry(self, strategy_result: StrategyRunResult, today_date: datetime):
        today_np = np.datetime64(today_date)
        signal_map = dict(zip(strategy_result.time, strategy_result.buy_signal))
        print("signal_map")
        print(signal_map.get(today_np, False))


class TradeOrchestrator:
    symbols: list[str]
    start_date: datetime
    end_date: datetime
    strategy_name: str
    traders: dict[str, TradeManager] = {}
    _last_run_date: date | None = None

    def __init__(
        self,
        symbols: list[str],
        strategy_name: str,
        start_date: datetime,
        end_date: datetime | None = None,
    ) -> None:
        self.symbols = symbols
        self.start_date = start_date
        self.end_date = end_date or datetime.now()
        self.strategy_name = strategy_name
        self.traders: dict[str, TradeManager] = {
            symbol: TradeManager([]) for symbol in symbols
        }

    def on_price_tick(self):
        for symbol in self.symbols:
            result = run_strategy(
                symbol, self.strategy_name, self.start_date, self.end_date
            )
            print(f"Symbol ---> {symbol}")
            self.traders[symbol].check_entry(result, self.end_date)
            print("---")

    def run_daily(self):
        """
        Wrapper to run on_price_tick **once per new day**
        """
        today = datetime.now().date()
        if self._last_run_date != today:
            self._last_run_date = today
            self.end_date = datetime.now()
            self.on_price_tick()

    def _run_for_date(self, date_to_run: datetime):
        """
        Run strategy and trade checks for a single date (end-of-day simulation)
        """
        if (date_to_run - self.start_date).days <= 2:
            return
        for symbol in self.symbols:
            result = run_strategy(
                symbol, self.strategy_name, self.start_date, date_to_run
            )
            self.traders[symbol].check_entry(result, date_to_run)
