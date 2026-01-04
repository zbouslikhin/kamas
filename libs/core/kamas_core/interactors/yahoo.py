from kamas_core.interactors.constants import Symbols, Timeframes
from datetime import datetime

import yfinance as yf
import pandas as pd

YAHOO_SYMBOLS = {Symbols.EURUSD: "EURUSD=X"}

YAHOO_TIMEFRAMES = {Timeframes.D1: "1d"}


def get_rates_yahoo(
    symbol: Symbols,
    date_start: datetime,
    date_end: datetime,
    timeframe: Timeframes,
) -> pd.DataFrame:
    try:
        df = yf.download(
            symbol,
            start=date_start,
            end=date_end,
            interval=timeframe,
            auto_adjust=False,
            progress=False,
        )

        df.reset_index(inplace=True)
        df.columns = [f"{i[0].lower()}" for i in df.columns]

        df["tick_volume"] = df["volume"]

        return df[["date", "high", "low", "open", "close", "tick_volume"]].rename(
            columns={"date": "time"}
        )
    except:
        raise ValueError("Non working day?")
