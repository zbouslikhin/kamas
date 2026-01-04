import attr
import datetime as dt


@attr.s(auto_attribs=True, frozen=True)
class TradeEvent:
    type: str  # "entry" | "exit"
    index: int
    time: dt.datetime
    price: float
