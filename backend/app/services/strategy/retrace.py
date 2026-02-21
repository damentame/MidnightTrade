def detect_retrace_touch(candles: list[dict], fvg_low: float, fvg_high: float, formed_ts) -> dict | None:
    for candle in candles:
        if candle["ts"] <= formed_ts:
            continue
        if candle["high"] >= fvg_low and candle["low"] <= fvg_high:
            return {"retrace_ts": candle["ts"], "candle": candle}
    return None
