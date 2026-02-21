def find_sweep(candles: list[dict], swings: list[dict], trend: str, lookback: int, max_age: int) -> dict | None:
    recent = swings[-lookback:]
    segment = candles[-max_age:]
    for candle in reversed(segment):
        if trend == "bull":
            lows = [s for s in recent if s["type"] == "low"]
            for s in lows:
                if candle["low"] < s["price"] and candle["close"] > s["price"]:
                    return {"swept_level_price": s["price"], "swing_index": s["index"], "sweep_candle_ts": candle["ts"], "candle": candle}
        elif trend == "bear":
            highs = [s for s in recent if s["type"] == "high"]
            for s in highs:
                if candle["high"] > s["price"] and candle["close"] < s["price"]:
                    return {"swept_level_price": s["price"], "swing_index": s["index"], "sweep_candle_ts": candle["ts"], "candle": candle}
    return None
