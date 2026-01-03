import attr
import datetime


@attr.s(auto_attribs=True)
class Trade:
    entry_price: float
    entry_time: datetime.datetime
    entry_index: int

    exit_price: float | None = None
    exit_time: datetime.datetime | None = None
    exit_index: int | None = None

    is_open: bool = True