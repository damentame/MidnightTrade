from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.bot_settings import BotSettings
from app.schemas.settings import SettingsUpdate

router = APIRouter(prefix="/api/settings", tags=["settings"])


@router.get("")
def get_settings(db: Session = Depends(get_db)):
    s = db.get(BotSettings, 1)
    if not s:
        raise HTTPException(404, "settings not initialized")
    return {"trading_enabled": s.trading_enabled, "risk_pct": float(s.risk_pct), "max_concurrent_positions": s.max_concurrent_positions}


@router.put("")
def update_settings(payload: SettingsUpdate, db: Session = Depends(get_db)):
    s = db.get(BotSettings, 1)
    if not s:
        s = BotSettings(id=1)
        db.add(s)
    for field in ["trading_enabled", "risk_pct", "max_concurrent_positions"]:
        val = getattr(payload, field)
        if val is not None:
            setattr(s, field, val)
    db.commit()
    db.refresh(s)
    return {"trading_enabled": s.trading_enabled, "risk_pct": float(s.risk_pct), "max_concurrent_positions": s.max_concurrent_positions}
