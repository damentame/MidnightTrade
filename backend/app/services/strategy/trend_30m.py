def detect_trend(swings: list[dict], n: int = 2) -> str:
    highs = [s["price"] for s in swings if s["type"] == "high"][-n:]
    lows = [s["price"] for s in swings if s["type"] == "low"][-n:]
    if len(highs) < n or len(lows) < n:
        return "range"
    if all(highs[i] > highs[i - 1] for i in range(1, n)) and all(lows[i] > lows[i - 1] for i in range(1, n)):
        return "bull"
    if all(highs[i] < highs[i - 1] for i in range(1, n)) and all(lows[i] < lows[i - 1] for i in range(1, n)):
        return "bear"
    return "range"
