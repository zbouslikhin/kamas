from datetime import datetime, timedelta, date

from kamas_core.api import run_strategy
from kamas_trader.orchestrator import TradeOrchestrator

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

    # def test_daily(self, start_date: datetime, end_date: datetime):
    #     start_date = start_date.replace(hour=1, second=0, microsecond=0)
    #     end_date = end_date.replace(hour=1, second=0, microsecond=0)
    #     current = start_date.replace(hour=2, second=0, microsecond=0)
    #     while current <= end_date:

    #         self.orchestrator._run_for_date(start_date, current)
    #         current += timedelta(days=1)
    #         input()

    def test_daily(self, start: datetime, end: datetime) -> None:
        current = start
        while current <= end:
            print("------")
            print(f"start date: {start}, today's date: {current}")
            print(f"end {end}")
            self.orchestrator._run_for_date(start, current)
            current += timedelta(days=1)
