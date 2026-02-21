def check_guards(trading_enabled: bool, spread_points: float, max_spread_points: float, sl_distance_points: float, min_sl_distance_points: float, open_positions: int, max_open: int):
    if not trading_enabled:
        return False, "trading_disabled"
    if spread_points > max_spread_points:
        return False, "spread_too_high"
    if sl_distance_points < min_sl_distance_points:
        return False, "sl_too_tight"
    if open_positions >= max_open:
        return False, "max_positions_reached"
    return True, "ok"
