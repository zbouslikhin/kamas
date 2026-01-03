import sys
from datetime import datetime, timezone

import pandas as pd
import requests

IS_WINDOWS = sys.platform == "win32"

# ===================== WINDOWS (MT5) =====================
if IS_WINDOWS:
    import MetaTrader5 as mt5

    DEFAULT_TIMEFRAME = mt5.TIMEFRAME_D1
else:
    DEFAULT_TIMEFRAME = "D"

# ===================== OANDA CONFIG =====================
OANDA_API_URL = "https://api-fxpractice.oanda.com/v3"  # demo
OANDA_TOKEN = "YOUR_OANDA_API_TOKEN"

# ===================== YAHOO =====================
import yfinance as yf


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
    symbol: str,
    date_start: datetime,
    date_end: datetime,
    timeframe,
) -> pd.DataFrame:
    initialize_mt5(
        server="OANDATMS-MT5",
        login=62478973,
        password="cg&kiTK1GsSeK1",
        path=r"C:\Program Files\OANDA TMS MT5 Terminal\terminal64.exe",
    )

    rates = mt5.copy_rates_range(symbol, timeframe, date_start, date_end)
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")

    return df[["time", "high", "low", "open", "close", "tick_volume"]]


# ===================== OANDA =====================
def get_rates_oanda(
    symbol: str,  # "EUR_USD"
    date_start: datetime,
    date_end: datetime,
    timeframe: str,  # "D", "H1", "M5"
) -> pd.DataFrame:
    headers = {
        "Authorization": f"Bearer {OANDA_TOKEN}",
        "Content-Type": "application/json",
    }

    params = {
        "from": date_start.replace(tzinfo=timezone.utc).isoformat(),
        "to": date_end.replace(tzinfo=timezone.utc).isoformat(),
        "granularity": timeframe,
        "price": "M",
    }

    r = requests.get(
        f"{OANDA_API_URL}/instruments/{symbol}/candles",
        headers=headers,
        params=params,
        timeout=30,
    )
    r.raise_for_status()

    rows = []
    for c in r.json()["candles"]:
        if not c["complete"]:
            continue
        rows.append(
            {
                "time": pd.to_datetime(c["time"]),
                "high": float(c["mid"]["h"]),
                "low": float(c["mid"]["l"]),
                "close": float(c["mid"]["c"]),
                "tick_volume": int(c["volume"]),
            }
        )

    return pd.DataFrame(rows)


# ===================== YAHOO (FALLBACK) =====================
def get_rates_yahoo(
    symbol: str,  # "EURUSD=X"
    date_start: datetime,
    date_end: datetime,
    timeframe: str,  # "1d", "1h"
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


# ===================== UNIFIED ENTRY =====================
def get_rates(
    symbol: str,
    date_start: datetime,
    date_end: datetime,
    timeframe=DEFAULT_TIMEFRAME,
) -> pd.DataFrame:
    if IS_WINDOWS:
        return get_rates_mt5(symbol, date_start, date_end, timeframe)

    # non-Windows priority: OANDA → Yahoo
    try:
        return get_rates_oanda(symbol, date_start, date_end, timeframe)
    except Exception:
        return get_rates_yahoo(symbol, date_start, date_end, "1d")
