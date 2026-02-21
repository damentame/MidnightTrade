from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes_ctrader import router as ctrader_router
from app.api.routes_health import router as health_router
from app.api.routes_settings import router as settings_router
from app.api.routes_signals import router as signals_router
from app.api.routes_stats import router as stats_router
from app.api.routes_trades import router as trades_router
from app.logging_config import setup_logging

setup_logging()
app = FastAPI(title="ctrader-xau-lsfvg-bot")

app.include_router(health_router)
app.include_router(settings_router)
app.include_router(signals_router)
app.include_router(trades_router)
app.include_router(stats_router)
app.include_router(ctrader_router)

static_dir = Path("/frontend/static")
if static_dir.exists():
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
