from pydantic import BaseModel


class OverviewStats(BaseModel):
    total_pnl: float
    win_rate: float
    trade_count: int
    avg_r: float
    expectancy: float
    profit_factor: float
    max_drawdown: float
    equity_curve: list[dict]
    bos_occurrence_rate: float
