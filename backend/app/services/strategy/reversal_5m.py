def _body(c):
    return abs(c["close"] - c["open"])


def _wick_ratio(c):
    body = _body(c) or 1e-9
    wick = (c["high"] - max(c["open"], c["close"])) + (min(c["open"], c["close"]) - c["low"])
    return wick / body


def detect_reversal(candles: list[dict], trend: str, retrace_ts, fvg_low: float, fvg_high: float, wick_ratio=2.0, body_ratio=0.4, strong_close_pct=0.2):
    zone = max(fvg_high - fvg_low, 1e-9)
    for i in range(1, len(candles)):
        prev, cur = candles[i - 1], candles[i]
        if cur["ts"] <= retrace_ts:
            continue
        prev_low_b, prev_high_b = sorted([prev["open"], prev["close"]])
        cur_low_b, cur_high_b = sorted([cur["open"], cur["close"]])
        bull_engulf = cur["close"] > cur["open"] and cur_low_b <= prev_low_b and cur_high_b >= prev_high_b
        bear_engulf = cur["close"] < cur["open"] and cur_low_b <= prev_low_b and cur_high_b >= prev_high_b
        if trend == "bull" and bull_engulf:
            return {"type": "engulfing", "candle_ts": cur["ts"], "candle": cur}
        if trend == "bear" and bear_engulf:
            return {"type": "engulfing", "candle_ts": cur["ts"], "candle": cur}
        if _wick_ratio(cur) >= wick_ratio and (_body(cur) / max((cur["high"] - cur["low"]), 1e-9)) <= body_ratio:
            return {"type": "pinbar", "candle_ts": cur["ts"], "candle": cur, "thresholds": {"wick_ratio": wick_ratio, "body_ratio": body_ratio}}
        if trend == "bull" and cur["close"] > fvg_high + zone * strong_close_pct:
            return {"type": "strong_close", "candle_ts": cur["ts"], "candle": cur}
        if trend == "bear" and cur["close"] < fvg_low - zone * strong_close_pct:
            return {"type": "strong_close", "candle_ts": cur["ts"], "candle": cur}
    return None
