from app.config import settings
from app.models.orders import OrderStatus
from app.models.signals import SignalStatus
from app.services.execution.order_manager import create_order_from_signal
from app.services.risk.guards import check_guards
from app.services.risk.sizing import compute_volume


def execute_signal(db, adapter, signal, bot_settings):
    if signal.status != SignalStatus.CONFIRMED:
        return None
    symbol_info = adapter.get_symbol_info(signal.symbol)
    acct = adapter.get_account_state()
    entry = float(signal.entry_level)
    if signal.trend_30m.value == "bull":
        sl = min(signal.fvg_json["fvg_low"], signal.sweep_json["swept_level_price"]) - settings.sl_buffer_points * symbol_info["tick_size"]
        tp = entry + 2 * (entry - sl)
        late = acct.get("equity", entry) > entry
    else:
        sl = max(signal.fvg_json["fvg_high"], signal.sweep_json["swept_level_price"]) + settings.sl_buffer_points * symbol_info["tick_size"]
        tp = entry - 2 * (sl - entry)
        late = acct.get("equity", entry) < entry
    if late and not settings.allow_late_entry:
        signal.status = SignalStatus.SKIPPED_LATE
        return None
    sl_distance_points = abs(entry - sl) / symbol_info["tick_size"]
    ok, reason = check_guards(bot_settings.trading_enabled, symbol_info["spread_points"], settings.max_spread_points, sl_distance_points, settings.min_sl_distance_points, acct.get("open_positions", 0), bot_settings.max_concurrent_positions)
    if not ok:
        signal.explain_json["guard_failure"] = reason
        return None
    volume, sizing = compute_volume(acct["balance"], float(bot_settings.risk_pct), entry, sl, symbol_info["tick_size"], symbol_info["tick_value"], symbol_info["min_volume"], symbol_info["volume_step"])
    order = create_order_from_signal(signal, volume, sl, tp)
    broker_resp = adapter.place_stop_order(symbol=signal.symbol, entry=entry, sl=sl, tp=tp, volume=volume, side=order.order_type.value)
    order.status = OrderStatus.PLACED
    order.broker_order_id = broker_resp["broker_order_id"]
    order.broker_response_json = broker_resp
    signal.status = SignalStatus.ORDER_PLACED
    signal.explain_json["sizing"] = sizing
    db.add(order)
    return order
