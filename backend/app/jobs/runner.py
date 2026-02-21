from apscheduler.schedulers.blocking import BlockingScheduler
from sqlalchemy.orm import Session

from app.config import settings
from app.db import SessionLocal
from app.models.bot_settings import BotSettings
from app.models.equity_snapshots import EquitySnapshot
from app.models.signals import Signal, SignalStatus, Trend
from app.services.broker.ctrader_openapi_adapter import CTraderOpenApiAdapter
from app.services.execution.executor import execute_signal
from app.services.reporting.equity import compute_drawdown
from app.services.strategy.signal_engine import generate_signal


def cycle():
    db: Session = SessionLocal()
    try:
        adapter = CTraderOpenApiAdapter()
        s = db.get(BotSettings, 1)
        if not s:
            s = BotSettings(id=1, trading_enabled=settings.trading_enabled, risk_pct=settings.risk_pct_default, max_concurrent_positions=settings.max_concurrent_positions)
            db.add(s)
            db.commit()
            db.refresh(s)
        c5 = adapter.fetch_candles(settings.symbol, "5m", 300)
        c30 = adapter.fetch_candles(settings.symbol, "30m", 200)
        built = generate_signal(c30, c5)
        if built:
            signal = Signal(
                symbol=built["symbol"],
                expires_at=built["expires_at"],
                trend_30m=Trend(built["trend"]),
                sweep_json=built["sweep"],
                fvg_json=built["fvg"],
                entry_level=built["entry_level"],
                retrace_ts=built["retrace_ts"],
                reversal_json=built["reversal"],
                bos_json=built["bos"],
                bos_occurred=built["bos_occurred"],
                status=SignalStatus.CONFIRMED,
                explain_json=built["explain"],
            )
            db.add(signal)
            db.flush()
            execute_signal(db, adapter, signal, s)
        acct = adapter.get_account_state()
        last = db.query(EquitySnapshot).order_by(EquitySnapshot.ts.desc()).first()
        peak = max(float(last.equity), acct["equity"]) if last else acct["equity"]
        db.add(EquitySnapshot(balance=acct["balance"], equity=acct["equity"], drawdown=compute_drawdown(acct["equity"], peak)))
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(cycle, "interval", seconds=60)
    scheduler.start()
