# api/app.py
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select

from dashboard.engine import engine
from dashboard.models import StrategyRun

app = FastAPI(title="kamasTrainer Dashboard")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        "runs.html",
        {"request": request},
    )


@app.get("/runs", response_class=HTMLResponse)
def runs_table(request: Request):
    with Session(engine) as session:
        runs = session.exec(
            select(StrategyRun).order_by(StrategyRun.created_at.desc())
        ).all()

    return templates.TemplateResponse(
        "runs_table.html",
        {
            "request": request,
            "runs": runs,
        },
    )
