import datetime as dt

from kamas_core.time import normalize_time
from kamas_core.interactors.mt5 import get_rates_mt5


def test_get_rates():
    import MetaTrader5 as mt5

    symbol = "EURUSD"
    start = normalize_time(dt.datetime(2025, 10, 6))
    end = normalize_time(dt.datetime(2025, 10, 10, hour=23, minute=59, second=59))

    rates_df = get_rates_mt5(symbol, start, end, mt5.TIMEFRAME_D1)
    inclusive_range = (end - start).days + 1
    assert len(rates_df["time"]) == inclusive_range
