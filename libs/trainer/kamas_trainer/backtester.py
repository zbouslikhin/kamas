from datetime import datetime
from typing import Tuple, List, Dict, Any

import numpy as np

from kamas_trainer.simulate import simulate_trades
from kamas_core.api import run_strategy


def draft_backtest(
    symbol: str,
    strategy_name: str,
    start: datetime,
    end: datetime,
    initial_balance: float = 1000.0,
):
    result = run_strategy(
        symbol=symbol,
        strategy_name=strategy_name,
        start=start,
        end=end,
    )

    balance, profit, trades = simulate_trades(
        prices=result.price_close,
        buy=result.buy_signal,
        initial_balance=initial_balance,
    )

    return {
        "final_balance": balance,
        "profit": profit,
        "trades": trades,
    }


class SimpleBacktester:
    def __init__(
        self,
        close: np.ndarray,
        buy_signal: np.ndarray,
        sell_signal: np.ndarray,
        initial_balance: float = 1000.0,
        commission: float = 0.0,
    ) -> None:
        self.close = close
        self.buy = buy_signal.astype(bool)
        self.sell = sell_signal.astype(bool)
        self.initial_balance = initial_balance
        self.commission = commission

    def run(self) -> Tuple[float, float, List[Dict[str, float]]]:
        return simulate_trades(
            prices=self.close,
            buy=self.buy,
            sell=self.sell,
            initial_balance=self.initial_balance,
            commission=self.commission,
        )