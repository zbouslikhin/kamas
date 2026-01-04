from typing import Callable, Dict

from kamas_core.critters.indicators import sma, ema, atr
from kamas_core.critters.operators import gt, lt, and_, or_, sub, div, eq
from kamas_core.critters.aggregators import weighted_vote

MODEL_REGISTRY: Dict[str, Callable] = {
    "sma": sma,
    "ema": ema,
    "atr": atr,
    "gt": gt,
    "lt": lt,
    "and": and_,
    "eq": eq,
    "or": or_,
    "sub": sub,
    "div": div,
    "weighted_vote": weighted_vote,
}
