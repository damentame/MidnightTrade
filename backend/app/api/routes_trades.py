from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.trades import Trade

router = APIRouter(prefix="/api/trades", tags=["trades"])


@router.get("")
def list_trades(db: Session = Depends(get_db)):
    return db.query(Trade).order_by(Trade.open_time.desc()).limit(500).all()


@router.get("/{trade_id}")
def get_trade(trade_id: str, db: Session = Depends(get_db)):
    return db.query(Trade).filter(Trade.id == trade_id).first()
