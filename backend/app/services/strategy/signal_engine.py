from datetime import datetime, timedelta

from app.config import settings
from app.services.data.swings import detect_swings
from app.services.strategy.bos_5m import detect_bos
from app.services.strategy.explain import build_explain
from app.services.strategy.fvg_5m import find_fvg
from app.services.strategy.retrace import detect_retrace_touch
from app.services.strategy.reversal_5m import detect_reversal
from app.services.strategy.sweep_5m import find_sweep
from app.services.strategy.trend_30m import detect_trend


def generate_signal(c30: list[dict], c5: list[dict]) -> dict | None:
    swings30 = detect_swings(c30, settings.swing_l)
    trend = detect_trend(swings30, settings.trend_n)
    if trend == "range":
        return None
    swings5 = detect_swings(c5, settings.swing_l)
    sweep = find_sweep(c5, swings5, trend, settings.sweep_swing_lookback, settings.sweep_max_age_candles)
    if not sweep:
        return None
    fvg = find_fvg(c5, trend, after_ts=sweep["sweep_candle_ts"] if settings.fvg_must_be_after_sweep else None)
    if not fvg:
        return None
    retrace = detect_retrace_touch(c5, fvg["fvg_low"], fvg["fvg_high"], fvg["formed_ts"])
    if not retrace:
        return None
    reversal = detect_reversal(c5, trend, retrace["retrace_ts"], fvg["fvg_low"], fvg["fvg_high"], settings.pinbar_wick_ratio, settings.pinbar_body_ratio, settings.strong_close_zone_pct)
    if not reversal:
        return None
    if trend == "bull":
        candidates = sorted([s for s in swings5 if s["type"] == "high" and s["price"] > fvg["fvg_high"]], key=lambda x: x["price"])
    else:
        candidates = sorted([s for s in swings5 if s["type"] == "low" and s["price"] < fvg["fvg_low"]], key=lambda x: x["price"], reverse=True)
    if not candidates:
        return None
    entry_swing = candidates[0]
    bos = detect_bos(c5, swings5, trend)
    explain = build_explain(trend=trend, sweep=sweep, fvg=fvg, retrace=retrace, reversal=reversal, bos=bos)
    return {
        "symbol": settings.symbol,
        "created_at": datetime.utcnow(),
        "expires_at": datetime.utcnow() + timedelta(minutes=settings.signal_ttl_minutes),
        "trend": trend,
        "sweep": sweep,
        "fvg": fvg,
        "entry_level": entry_swing["price"],
        "retrace_ts": retrace["retrace_ts"],
        "reversal": reversal,
        "bos": bos,
        "bos_occurred": bool(bos),
        "explain": explain,
    }
