from kamas_trader.models import Trade


def stop_loss(trade: Trade, price: float, pct: float) -> bool:
    return price <= trade.entry_price * (1 - pct)


def take_profit(trade: Trade, price: float, pct: float) -> bool:
    return price >= trade.entry_price * (1 + pct)

