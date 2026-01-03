from typing import Dict, List, Tuple

import numpy as np


def simulate_trades(
    prices: np.ndarray,
    buy: np.ndarray,
    initial_balance: float = 1000.0,
    commission: float = 0.0,
) -> Tuple[float, float, List[Dict[str, float]]]:
    """
    Core trade execution logic.
    Shared by all backtesting modes.
    """

    balance = initial_balance
    position = 0.0
    trades: List[Dict[str, float]] = []

    for i in range(len(prices)):
        price = prices[i]

        if buy[i] and position == 0.0:
            position = balance / price
            balance -= position * price * commission
            trades.append({"type": "buy", "price": price, "index": i})

    # close open position
    if position > 0.0:
        balance = position * prices[-1]
        trades.append({"type": "sell", "price": prices[-1], "index": len(prices) - 1})

    profit = balance - initial_balance
    return balance, profit, trades

