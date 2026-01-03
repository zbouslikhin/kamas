# api/app.py
from kamas_dashboard.models import StrategyRun
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


from kamas_dashboard.db import engine, create_db_and_tables
from kamas_dashboard.views import router 

create_db_and_tables()

app = FastAPI(title="kamasTrainer Dashboard", description="API for serving predictions from an ML model.")
app.include_router(router)
