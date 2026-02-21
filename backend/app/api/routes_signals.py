from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.signals import Signal

router = APIRouter(prefix="/api/signals", tags=["signals"])


@router.get("")
def list_signals(status: str | None = None, db: Session = Depends(get_db)):
    q = db.query(Signal)
    if status:
        q = q.filter(Signal.status == status)
    return q.order_by(Signal.created_at.desc()).limit(500).all()


@router.get("/{signal_id}")
def get_signal(signal_id: str, db: Session = Depends(get_db)):
    return db.query(Signal).filter(Signal.id == signal_id).first()
