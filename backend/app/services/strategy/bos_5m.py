def detect_bos(candles: list[dict], post_sweep_swings: list[dict], trend: str):
    if not post_sweep_swings:
        return None
    if trend == "bull":
        highs = [s for s in post_sweep_swings if s["type"] == "high"]
        if highs:
            lvl = highs[-1]["price"]
            for c in candles:
                if c["close"] > lvl:
                    return {"direction": "bull", "break_level": lvl, "ts": c["ts"]}
    if trend == "bear":
        lows = [s for s in post_sweep_swings if s["type"] == "low"]
        if lows:
            lvl = lows[-1]["price"]
            for c in candles:
                if c["close"] < lvl:
                    return {"direction": "bear", "break_level": lvl, "ts": c["ts"]}
    return None
