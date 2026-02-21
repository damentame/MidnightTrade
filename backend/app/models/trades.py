import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, JSON, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Direction(str, enum.Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class Outcome(str, enum.Enum):
    WIN = "WIN"
    LOSS = "LOSS"
    BREAKEVEN = "BREAKEVEN"
    OPEN = "OPEN"


class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("signals.id"))
    broker_position_id: Mapped[str] = mapped_column(String(128), unique=True)
    symbol: Mapped[str] = mapped_column(String(32), nullable=False)
    direction: Mapped[Direction] = mapped_column(Enum(Direction), nullable=False)
    entry_price: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    sl: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    tp: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    volume: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    open_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    close_time: Mapped[datetime | None] = mapped_column(DateTime)
    close_price: Mapped[float | None] = mapped_column(Numeric(18, 8))
    pnl_usd: Mapped[float | None] = mapped_column(Numeric(18, 8))
    pnl_r: Mapped[float | None] = mapped_column(Numeric(18, 8))
    slippage_points: Mapped[float | None] = mapped_column(Numeric(18, 8))
    outcome: Mapped[Outcome] = mapped_column(Enum(Outcome), default=Outcome.OPEN)
    execution_meta_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
