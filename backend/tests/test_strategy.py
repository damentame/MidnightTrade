from datetime import datetime, timedelta

from app.services.data.swings import detect_swings
from app.services.strategy.bos_5m import detect_bos
from app.services.strategy.fvg_5m import find_fvg
from app.services.strategy.reversal_5m import detect_reversal
from app.services.strategy.trend_30m import detect_trend


def mk(prices):
    t = datetime(2024, 1, 1)
    out = []
    for i, p in enumerate(prices):
        out.append({"ts": t + timedelta(minutes=5 * i), "open": p, "high": p + 1, "low": p - 1, "close": p + 0.2})
    return out


def test_swings_detect():
    candles = mk([1, 2, 5, 2, 1, 3, 4, 3, 1])
    swings = detect_swings(candles, 1)
    assert any(s["type"] == "high" for s in swings)
    assert any(s["type"] == "low" for s in swings)


def test_trend_detection_bull():
    swings = [{"type": "high", "price": 10}, {"type": "low", "price": 8}, {"type": "high", "price": 12}, {"type": "low", "price": 9}]
    assert detect_trend(swings, 2) == "bull"


def test_fvg_detection():
    c = [
        {"ts": 1, "open": 1, "high": 10, "low": 8, "close": 9},
        {"ts": 2, "open": 9, "high": 11, "low": 9, "close": 10},
        {"ts": 3, "open": 12, "high": 13, "low": 10.5, "close": 12.5},
    ]
    assert find_fvg(c, "bull") is not None


def test_reversal_detection_engulfing():
    candles = [
        {"ts": 1, "open": 10, "high": 10.3, "low": 9.5, "close": 9.6},
        {"ts": 2, "open": 9.5, "high": 10.8, "low": 9.4, "close": 10.7},
    ]
    rv = detect_reversal(candles, "bull", 0, 9.7, 10.2)
    assert rv and rv["type"] in {"engulfing", "pinbar", "strong_close"}


def test_bos_detection():
    candles = [{"ts": 1, "close": 11}, {"ts": 2, "close": 13}]
    swings = [{"type": "high", "price": 12}]
    assert detect_bos(candles, swings, "bull") is not None
