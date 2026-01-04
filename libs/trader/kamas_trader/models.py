import datetime as dt

import attr


@attr.s(auto_attribs=True)
class Trade:
    entry_price: float
    entry_time: dt.datetime

    exit_price: float | None = None
    exit_time: dt.datetime | None = None

    @property
    def is_open(self) -> bool:
        return self.exit_time is None

    @property
    def pnl(self) -> float | None:
        if self.exit_price is not None:
            return self.exit_price - self.entry_price
        return None
