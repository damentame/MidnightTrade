import math


def compute_volume(balance, risk_pct, entry, sl, tick_size, tick_value, min_volume, volume_step):
    risk_usd = balance * risk_pct
    sl_distance = abs(entry - sl)
    ticks = sl_distance / tick_size
    loss_per_1_volume = ticks * tick_value
    raw_volume = risk_usd / max(loss_per_1_volume, 1e-9)
    volume = math.floor(raw_volume / volume_step) * volume_step
    volume = max(volume, min_volume)
    return volume, {"risk_usd": risk_usd, "sl_distance": sl_distance, "ticks": ticks, "loss_per_1_volume": loss_per_1_volume, "raw_volume": raw_volume}
