from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class BotSettings(Base):
    __tablename__ = "bot_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    trading_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    risk_pct: Mapped[float] = mapped_column(Numeric(5, 4), default=0.10, nullable=False)
    max_concurrent_positions: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
