from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class StrategyRun(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    strategy_name: str
    symbol: str
    final_balance: float
    profit: float
    created_at: datetime = Field(default_factory=datetime.utcnow)