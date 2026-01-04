import datetime as dt
from zoneinfo import ZoneInfo

TZ = ZoneInfo("UTC")


def normalize_time(date: dt.datetime) -> dt.datetime:
    if date.tzinfo is None:
        date = date.replace(tzinfo=TZ)

    return date.astimezone(TZ)


def today() -> dt.datetime:
    now = dt.datetime.now()
    return dt.datetime(year=now.year, month=now.month, day=now.day, tzinfo=TZ)
