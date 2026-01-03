import datetime
from pathlib import Path

import attr
from fastapi import APIRouter, FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from kamas_core.engine.loader import load_strategy
from kamas_core.engine.schema import Strategy
from kamas_trader.trader import TradeOrchestrator
from kamas_trainer.backtester import SimpleBacktester, draft_backtest
from kamas_trainer.periods import STRESS_PERIODS
from sqlmodel import Session, select

from kamas_dashboard.db import StrategyRunDB, create_db_and_tables, engine
from kamas_dashboard.helpers import strategy_to_mermaid
from kamas_dashboard.models import StrategyRun

PROJECT_ROOT = Path(__file__).resolve().parents[2]
TEMPLATES_DIR = PROJECT_ROOT / "templates"

router = APIRouter()


def get_templates():
    return Jinja2Templates(directory=TEMPLATES_DIR)


@router.get("/", response_class=HTMLResponse)
def home(request: Request, templates=get_templates()):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


@router.get("/runs", response_class=HTMLResponse)
async def runs_table(request: Request, templates=get_templates()):
    with Session(engine) as session:
        runs = session.exec(
            select(StrategyRunDB).order_by(StrategyRunDB.created_at.desc())
        ).all()

    return templates.TemplateResponse(
        "components/runs_table.html",
        {
            "request": request,
            "runs": runs,
        },
    )


# @router.post("/make", response_model=StrategyRunDB)
# async def make_prediction(data: StrategyRun):
#     """
#     Accepts input data, creates a prediction, saves it to the DB,
#     and returns the saved DB object.
#     """

#     final_balance = 2.0        # Replace with your model prediction
#     profit = 3.0               # Replace if your model provides profit info

#     new_run = StrategyRunDB(
#         strategy_name=data.strategy_name,
#         symbol=data.symbol,
#         final_balance=final_balance,
#         profit=profit,
#         created_at=datetime.datetime.now()
#     )

#     with Session(engine) as session:
#         session.add(new_run)
#         session.commit()
#         session.refresh(new_run)

#     return new_run


@router.get("/strategy/{strategy_file}/graph", response_class=HTMLResponse)
def show_graph(request: Request, strategy_file: str, templates=get_templates()):
    strategy = load_strategy(strategy_file)
    mermaid_code = strategy_to_mermaid(strategy)
    return templates.TemplateResponse(
        "strategy_graph.html",
        {
            "request": request,
            "mermaid_code": mermaid_code,
            "strategy_name": strategy.name,
        },
    )


@router.get("/strategy/{strategy_file}/test", response_class=HTMLResponse)
def test_strategy(
    request: Request,
    strategy_file: str,
    # symbol: str = "EURUSD.pro",
    symbol: str = "EURUSD=X",
    templates=get_templates(),
):
    start = STRESS_PERIODS["COVID_CRASH"].start
    start = datetime.datetime.now() - datetime.timedelta(days=90)
    end = datetime.datetime.now()
    initial_balance = 1000.0

    orchestrator = TradeOrchestrator([symbol], strategy_file, start)
    backtester = SimpleBacktester(orchestrator)
    backtester.start(end)

    result = draft_backtest(
        symbol=symbol,
        strategy_name=strategy_file,
        start=start,
        end=end,
        initial_balance=initial_balance,
    )

    summary = {
        "start": start,
        "end": end,
        "initial_balance": initial_balance,
        "final_balance": result["final_balance"],
        "profit": result["profit"],
        "trades_count": len(result["trades"]),
    }

    return templates.TemplateResponse(
        "strategy_test.html",
        {
            "request": request,
            "strategy_name": strategy_file,
            "symbol": symbol,
            "summary": summary,
            "trades": result["trades"],
        },
    )
