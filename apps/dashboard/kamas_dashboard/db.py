from sqlmodel import create_engine
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

engine = create_engine(
    "sqlite:///kamastrainer.db",
    echo=False,
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

class StrategyRunDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    strategy_name: str
    symbol: str
    final_balance: float
    profit: float
    created_at: datetime