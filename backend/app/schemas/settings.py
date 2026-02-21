from pydantic import BaseModel, Field


class SettingsOut(BaseModel):
    trading_enabled: bool
    risk_pct: float
    max_concurrent_positions: int


class SettingsUpdate(BaseModel):
    trading_enabled: bool | None = None
    risk_pct: float | None = Field(default=None, ge=0.001, le=1.0)
    max_concurrent_positions: int | None = Field(default=None, ge=1, le=10)
