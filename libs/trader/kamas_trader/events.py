import attr
import datetime


@attr.s(auto_attribs=True, frozen=True)
class TradeEvent:
    type: str               # "entry" | "exit"
    index: int
    time: datetime.datetime
    price: float