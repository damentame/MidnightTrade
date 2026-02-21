import enum
import uuid
from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Enum, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Trend(str, enum.Enum):
    bull = "bull"
    bear = "bear"
    range = "range"


class SignalStatus(str, enum.Enum):
    CREATED = "CREATED"
    ARMED = "ARMED"
    TOUCHED = "TOUCHED"
    CONFIRMED = "CONFIRMED"
    ORDER_PLACED = "ORDER_PLACED"
    ENTERED = "ENTERED"
    CLOSED = "CLOSED"
    EXPIRED = "EXPIRED"
    INVALIDATED = "INVALIDATED"
    SKIPPED_LATE = "SKIPPED_LATE"


class Signal(Base):
    __tablename__ = "signals"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    symbol: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    trend_30m: Mapped[Trend] = mapped_column(Enum(Trend), nullable=False)
    sweep_json: Mapped[dict] = mapped_column(JSON, default=dict)
    fvg_json: Mapped[dict] = mapped_column(JSON, default=dict)
    entry_level: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    retrace_ts: Mapped[datetime | None] = mapped_column(DateTime)
    reversal_json: Mapped[dict | None] = mapped_column(JSON)
    bos_json: Mapped[dict | None] = mapped_column(JSON)
    bos_occurred: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[SignalStatus] = mapped_column(Enum(SignalStatus), default=SignalStatus.CREATED)
    explain_json: Mapped[dict] = mapped_column(JSON, default=dict)
    last_updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
