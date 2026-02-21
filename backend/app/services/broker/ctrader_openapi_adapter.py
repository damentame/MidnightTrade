from datetime import datetime, timedelta
import random

from app.services.broker.adapter import BrokerAdapter


class CTraderOpenApiAdapter(BrokerAdapter):
    """Adapter placeholder for Spotware OpenApiPy integration."""

    def __init__(self, access_token: str | None = None):
        self.access_token = access_token

    def fetch_candles(self, symbol: str, timeframe: str, limit: int) -> list[dict]:
        now = datetime.utcnow().replace(second=0, microsecond=0)
        step = 30 if timeframe == "30m" else 5
        candles = []
        price = 2300.0
        for i in range(limit):
            ts = now - timedelta(minutes=step * (limit - i))
            o = price + random.uniform(-2, 2)
            c = o + random.uniform(-2, 2)
            h = max(o, c) + random.uniform(0, 1.5)
            l = min(o, c) - random.uniform(0, 1.5)
            candles.append({"ts": ts, "open": o, "high": h, "low": l, "close": c})
            price = c
        return candles

    def get_symbol_info(self, symbol: str) -> dict:
        return {
            "symbol": symbol,
            "tick_size": 0.01,
            "tick_value": 1.0,
            "min_volume": 0.01,
            "volume_step": 0.01,
            "spread_points": 20,
        }

    def place_stop_order(self, **kwargs) -> dict:
        return {"broker_order_id": f"ord-{int(datetime.utcnow().timestamp())}", "status": "PLACED", "request": kwargs}

    def get_account_state(self) -> dict:
        return {"balance": 10000.0, "equity": 10000.0, "open_positions": 0}
