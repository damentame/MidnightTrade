def intersect_zone(candle: dict, low: float, high: float) -> bool:
    return candle["high"] >= low and candle["low"] <= high
