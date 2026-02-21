from datetime import datetime
from pydantic import BaseModel


class SignalOut(BaseModel):
    id: str
    symbol: str
    trend_30m: str
    status: str
    bos_occurred: bool
    created_at: datetime
    explain_json: dict
