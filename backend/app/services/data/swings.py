def detect_swings(candles: list[dict], l: int) -> list[dict]:
    swings = []
    for i in range(l, len(candles) - l):
        highs = [candles[j]["high"] for j in range(i - l, i + l + 1)]
        lows = [candles[j]["low"] for j in range(i - l, i + l + 1)]
        if candles[i]["high"] == max(highs):
            swings.append({"index": i, "ts": candles[i]["ts"], "price": candles[i]["high"], "type": "high"})
        if candles[i]["low"] == min(lows):
            swings.append({"index": i, "ts": candles[i]["ts"], "price": candles[i]["low"], "type": "low"})
    return swings
