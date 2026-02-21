import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, JSON, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class OrderType(str, enum.Enum):
    BUY_STOP = "BUY_STOP"
    SELL_STOP = "SELL_STOP"
    MARKET = "MARKET"


class OrderStatus(str, enum.Enum):
    NEW = "NEW"
    PLACED = "PLACED"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    CANCELED = "CANCELED"
    EXPIRED = "EXPIRED"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    signal_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("signals.id"), unique=True)
    broker_order_id: Mapped[str | None] = mapped_column(String(128))
    order_type: Mapped[OrderType] = mapped_column(Enum(OrderType), nullable=False)
    requested_entry: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    requested_sl: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    requested_tp: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    requested_volume: Mapped[float] = mapped_column(Numeric(18, 8), nullable=False)
    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), default=OrderStatus.NEW)
    broker_response_json: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
