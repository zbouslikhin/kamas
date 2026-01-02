from kamas_trainer.critters.indicators import sma, ema, atr
from kamas_trainer.critters.operators import gt, lt, and_, or_, sub, div
from typing import Callable, Dict

MODEL_REGISTRY: Dict[str, Callable] = {
    "sma": sma,
    "ema": ema,
    "atr": atr,
    "gt": gt,
    "lt": lt,
    "and": and_,
    "or": or_,
    "sub": sub,
    "div": div,
}
