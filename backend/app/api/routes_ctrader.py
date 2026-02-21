import secrets

from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.bot_settings import BotSettings
from app.services.broker.ctrader_auth import exchange_code_for_token, get_auth_url

router = APIRouter(prefix="/api/ctrader", tags=["ctrader"])


@router.get("/auth/start")
def ctrader_auth_start():
    return RedirectResponse(get_auth_url(state=secrets.token_hex(8)))


@router.get("/callback")
def ctrader_callback(code: str, db: Session = Depends(get_db)):
    tokens = exchange_code_for_token(code)
    s = db.get(BotSettings, 1)
    if not s:
        s = BotSettings(id=1)
        db.add(s)
    db.commit()
    return {"status": "ok", "token_type": tokens["token_type"], "message": "tokens received; persist securely in production"}
