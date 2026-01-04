from kamas_core.time import normalize_time
from typing import NamedTuple, Dict
from datetime import datetime


class Period(NamedTuple):
    start: datetime
    end: datetime


STRESS_PERIODS: Dict[str, Period] = {
    "COVID_CRASH": Period(
        # COVID breakout officially on this day, but
        # start one year earlier to consider pre-crash
        # start=datetime(2020, 3, 11),
        start=normalize_time(datetime(2019, 3, 11)),
        end=normalize_time(datetime(2023, 5, 5)),
    ),
}
