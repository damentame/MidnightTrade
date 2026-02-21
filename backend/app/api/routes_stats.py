from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.equity_snapshots import EquitySnapshot
from app.models.trades import Trade
from app.services.reporting.metrics import overview_stats

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("/overview")
def stats_overview(db: Session = Depends(get_db)):
    trades = db.query(Trade).all()
    equity = db.query(EquitySnapshot).order_by(EquitySnapshot.ts.asc()).all()
    return overview_stats(trades, equity)


@router.get("/bos-split")
def bos_split(db: Session = Depends(get_db)):
    trades = db.query(Trade).all()
    with_bos = [t for t in trades if t.execution_meta_json.get("bos_occurred")]
    without_bos = [t for t in trades if not t.execution_meta_json.get("bos_occurred")]

    def agg(data):
        n = len(data)
        pnl = float(sum(float(t.pnl_usd or 0) for t in data))
        wins = len([t for t in data if (t.pnl_usd or 0) > 0])
        avg_r = float(sum(float(t.pnl_r or 0) for t in data) / n) if n else 0.0
        return {"count": n, "win_rate": (wins / n) if n else 0.0, "avg_r": avg_r, "pnl": pnl}

    return {"bos_true": agg(with_bos), "bos_false": agg(without_bos)}
