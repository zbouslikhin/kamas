import pandas as pd
from kamas_trainer.helpers import get_rates

class MarketFeeder:
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    def fetch(self) -> pd.DataFrame:
        rates = get_rates(self.symbol)
        return pd.DataFrame(rates)
