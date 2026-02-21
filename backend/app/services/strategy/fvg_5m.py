def find_fvg(candles: list[dict], trend: str, after_ts=None) -> dict | None:
    for i in range(2, len(candles)):
        c1, c3 = candles[i - 2], candles[i]
        if after_ts and c3["ts"] <= after_ts:
            continue
        if trend == "bull" and c1["high"] < c3["low"]:
            return {"fvg_low": c1["high"], "fvg_high": c3["low"], "formed_ts": c3["ts"], "direction": "bull", "indexes": [i - 2, i]}
        if trend == "bear" and c1["low"] > c3["high"]:
            return {"fvg_low": c3["high"], "fvg_high": c1["low"], "formed_ts": c3["ts"], "direction": "bear", "indexes": [i - 2, i]}
    return None
