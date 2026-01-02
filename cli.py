from kamas_trainer.helpers import initialize, get_rates
from kamas_trainer.engine.loader import load_strategy
from kamas_trainer.engine.builder import build_graph
from kamas_trainer.engine.context import GraphContext
from kamas_trainer.engine.utils import run_graph_on_df
from kamas_trainer.backtest.backtester import SimpleBacktester
import numpy as np

def main() -> None:
    initialize(
        server="OANDATMS-MT5",
        login=62478973,
        password="cg&kiTK1GsSeK1",
        path=r"C:\Program Files\OANDA TMS MT5 Terminal\terminal64.exe"
    )

    strategy = load_strategy("strategies/c1br1c2v.toml")
    rates = get_rates("EURUSD.pro")

    ctx = GraphContext(
        close=rates["close"],
        high=rates["high"],
        low=rates["low"],
        tick_volume=rates["tick_volume"]
    )

    graph = build_graph(strategy)
    outputs = graph.run(ctx)
    entry_signal = outputs[strategy.outputs["entry"]]

    bt = SimpleBacktester(close=ctx.close, signals=entry_signal, initial_balance=1000.0, commission=0.001)
    final_balance, profit, trades = bt.run()

    print(f"Final Balance: {final_balance:.2f}")
    print(f"Profit: {profit:.2f}")
    print(trades[-10:])

if __name__ == "__main__":
    main()
