"""init

Revision ID: 0001_init
Revises:
Create Date: 2026-01-01
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("bot_settings", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("trading_enabled", sa.Boolean(), nullable=False), sa.Column("risk_pct", sa.Numeric(5, 4), nullable=False), sa.Column("max_concurrent_positions", sa.Integer(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=True))
    op.create_table("signals", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("symbol", sa.String(32), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=True), sa.Column("expires_at", sa.DateTime(), nullable=False), sa.Column("trend_30m", sa.Enum("bull", "bear", "range", name="trend"), nullable=False), sa.Column("sweep_json", sa.JSON(), nullable=False), sa.Column("fvg_json", sa.JSON(), nullable=False), sa.Column("entry_level", sa.Numeric(18, 8), nullable=False), sa.Column("retrace_ts", sa.DateTime(), nullable=True), sa.Column("reversal_json", sa.JSON(), nullable=True), sa.Column("bos_json", sa.JSON(), nullable=True), sa.Column("bos_occurred", sa.Boolean(), nullable=True), sa.Column("status", sa.Enum("CREATED", "ARMED", "TOUCHED", "CONFIRMED", "ORDER_PLACED", "ENTERED", "CLOSED", "EXPIRED", "INVALIDATED", "SKIPPED_LATE", name="signalstatus"), nullable=True), sa.Column("explain_json", sa.JSON(), nullable=False), sa.Column("last_updated_at", sa.DateTime(), nullable=True))
    op.create_table("orders", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("signal_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("signals.id"), unique=True), sa.Column("broker_order_id", sa.String(128), nullable=True), sa.Column("order_type", sa.Enum("BUY_STOP", "SELL_STOP", "MARKET", name="ordertype"), nullable=False), sa.Column("requested_entry", sa.Numeric(18, 8), nullable=False), sa.Column("requested_sl", sa.Numeric(18, 8), nullable=False), sa.Column("requested_tp", sa.Numeric(18, 8), nullable=False), sa.Column("requested_volume", sa.Numeric(18, 8), nullable=False), sa.Column("status", sa.Enum("NEW", "PLACED", "FILLED", "REJECTED", "CANCELED", "EXPIRED", name="orderstatus"), nullable=True), sa.Column("broker_response_json", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=True), sa.Column("updated_at", sa.DateTime(), nullable=True))
    op.create_table("trades", sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True), sa.Column("signal_id", postgresql.UUID(as_uuid=True), sa.ForeignKey("signals.id"), nullable=True), sa.Column("broker_position_id", sa.String(128), nullable=False, unique=True), sa.Column("symbol", sa.String(32), nullable=False), sa.Column("direction", sa.Enum("LONG", "SHORT", name="direction"), nullable=False), sa.Column("entry_price", sa.Numeric(18, 8), nullable=False), sa.Column("sl", sa.Numeric(18, 8), nullable=False), sa.Column("tp", sa.Numeric(18, 8), nullable=False), sa.Column("volume", sa.Numeric(18, 8), nullable=False), sa.Column("open_time", sa.DateTime(), nullable=True), sa.Column("close_time", sa.DateTime(), nullable=True), sa.Column("close_price", sa.Numeric(18, 8), nullable=True), sa.Column("pnl_usd", sa.Numeric(18, 8), nullable=True), sa.Column("pnl_r", sa.Numeric(18, 8), nullable=True), sa.Column("slippage_points", sa.Numeric(18, 8), nullable=True), sa.Column("outcome", sa.Enum("WIN", "LOSS", "BREAKEVEN", "OPEN", name="outcome"), nullable=True), sa.Column("execution_meta_json", sa.JSON(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=True), sa.Column("updated_at", sa.DateTime(), nullable=True))
    op.create_table("equity_snapshots", sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True), sa.Column("ts", sa.DateTime(), nullable=True), sa.Column("balance", sa.Float(), nullable=False), sa.Column("equity", sa.Float(), nullable=False), sa.Column("drawdown", sa.Float(), nullable=True))
    op.create_table("events_log", sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True), sa.Column("ts", sa.DateTime(), nullable=True), sa.Column("level", sa.String(16), nullable=False), sa.Column("component", sa.String(64), nullable=False), sa.Column("message", sa.String(512), nullable=False), sa.Column("data_json", sa.JSON(), nullable=False))


def downgrade() -> None:
    op.drop_table("events_log")
    op.drop_table("equity_snapshots")
    op.drop_table("trades")
    op.drop_table("orders")
    op.drop_table("signals")
    op.drop_table("bot_settings")
