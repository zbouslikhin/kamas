import sys
from datetime import datetime, timezone, timedelta

import pandas as pd

from kamas_core.interactors.mt5 import get_rates_mt5
from kamas_core.interactors.yahoo import get_rates_yahoo
from kamas_core.interactors.oanda import get_rates_oanda
from kamas_core.interactors.constants import Timeframes, Symbols


IS_WINDOWS = sys.platform == "win32"


def get_rates(
    symbol: Symbols,
    date_start: datetime,
    date_end: datetime,
    timeframe: Timeframes = Timeframes.D1,
) -> pd.DataFrame:
    if IS_WINDOWS:
        return get_rates_mt5(symbol, date_start, date_end, timeframe)

    try:
        return get_rates_oanda(symbol, date_start, date_end, timeframe)
    except Exception:
        return get_rates_yahoo(symbol, date_start, date_end, "1d")
