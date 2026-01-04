import requests

import pandas as pd
from datetime import datetime, timezone

OANDA_API_URL = "https://api-fxpractice.oanda.com/v3"  # demo
OANDA_TOKEN = "YOUR_OANDA_API_TOKEN"


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
