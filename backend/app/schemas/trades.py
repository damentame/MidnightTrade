from datetime import datetime
from pydantic import BaseModel


class TradeOut(BaseModel):
    id: str
    symbol: str
    direction: str
    pnl_usd: float | None
    pnl_r: float | None
    outcome: str
    open_time: datetime
    close_time: datetime | None
