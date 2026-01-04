from kamas_core.interactors.constants import Timeframes, Symbols
from datetime import datetime, timezone, timedelta

import pandas as pd
import MetaTrader5 as mt5

DEFAULT_TIMEFRAME = mt5.TIMEFRAME_D1

MT5_SYMBOLS = {Symbols.EURUSD: "EURUSD.pro"}

MT5_TIMEFRAMES = {Timeframes.D1: mt5.TIMEFRAME_D1}


def initialize_mt5(server: str, login: int, password: str, path: str):
    if not mt5.initialize(
        path,
        login=login,
        server=server,
        password=password,
        timeout=300000,
    ):
        raise Exception(f"initialize() failed, error code {mt5.last_error()}")


def get_rates_mt5(
    symbol: Symbols,
    date_start: datetime,
    date_end: datetime,
    timeframe: Timeframes,
) -> pd.DataFrame:
    initialize_mt5(
        server="OANDATMS-MT5",
        login=62478973,
        password="cg&kiTK1GsSeK1",
        path=r"C:\Program Files\OANDA TMS MT5 Terminal\terminal64.exe",
    )

    if timeframe == mt5.TIMEFRAME_D1:
        # TODO: To get an inclusive range
        # e.g. 2025-10-06 -> 2025-10-10 (5 days)
        # 00:00 <= 23:59:59.999999 → always true
        date_start = date_start.replace(hour=0, minute=0, second=0)
        date_end = date_end.replace(hour=23, minute=59, second=59)
    print(MT5_SYMBOLS[symbol])
    rates = mt5.copy_rates_range(MT5_SYMBOLS[symbol], timeframe, date_start, date_end)
    df = pd.DataFrame(rates)

    df["time"] = pd.to_datetime(df["time"], unit="s")
    return df[["time", "high", "low", "open", "close", "tick_volume"]]
