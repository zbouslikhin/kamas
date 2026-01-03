from datetime import datetime, timedelta

from kamas_core.api import run_strategy
from kamas_trader.trader import TradeOrchestrator

from kamas_trainer.simulate import simulate_trades


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
        orchestrator: TradeOrchestrator,
        initial_balance: float = 1000.0,
        commission: float = 0.0,
    ) -> None:
        self.orchestrator = orchestrator
        self.initial_balance = initial_balance
        self.commission = commission

    def start(self, end_date: datetime):
        current = self.orchestrator.start_date
        while current <= end_date:
            print(f"Current {current}")
            print(f"end {end_date}")
            self.orchestrator._run_for_date(current)
            current += timedelta(days=1)

