from app.models.orders import Order, OrderType


def create_order_from_signal(signal, volume, sl, tp):
    order_type = OrderType.BUY_STOP if signal.trend_30m.value == "bull" else OrderType.SELL_STOP
    return Order(
        signal_id=signal.id,
        order_type=order_type,
        requested_entry=signal.entry_level,
        requested_sl=sl,
        requested_tp=tp,
        requested_volume=volume,
    )
