import numpy as np
from typing import Tuple, List, Dict

class SimpleBacktester:
    def __init__(self, close: np.ndarray, signals: np.ndarray, initial_balance: float = 1000.0, commission: float = 0.0) -> None:
        self.close = close
        self.signals = signals.astype(bool)
        self.initial_balance = initial_balance
        self.commission = commission
        self.trades: List[Dict[str, float]] = []

    def run(self) -> Tuple[float, float, List[Dict[str, float]]]:
        balance = self.initial_balance
        position = 0.0

        for i in range(len(self.signals)):
            signal = self.signals[i]
            price = self.close[i]

            if signal and position == 0.0:
                position = balance / price
                balance -= position * price * self.commission
                self.trades.append({"type": "buy", "price": price, "index": i})
            elif not signal and position > 0.0:
                balance = position * price
                balance -= position * price * self.commission
                self.trades.append({"type": "sell", "price": price, "index": i})
                position = 0.0

        if position > 0.0:
            balance = position * self.close[-1]
            self.trades.append({"type": "sell", "price": self.close[-1], "index": len(self.close)-1})

        profit = balance - self.initial_balance
        return balance, profit, self.trades
