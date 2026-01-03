from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class StrategyRun(BaseModel):
    id: int
    strategy_name: str
    symbol: str
    final_balance: float
    profit: float
    created_at: datetime
    