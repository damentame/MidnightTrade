from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.bot_settings import BotSettings

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health(db: Session = Depends(get_db)):
    s = db.get(BotSettings, 1)
    return {"status": "ok", "time": datetime.utcnow().isoformat(), "trading_enabled": bool(s.trading_enabled) if s else False}
