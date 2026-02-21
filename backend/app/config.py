from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_env: str = "dev"
    database_url: str
    log_level: str = "INFO"

    ctrader_client_id: str = ""
    ctrader_client_secret: str = ""
    ctrader_redirect_uri: str = "http://localhost:8000/api/ctrader/callback"
    ctrader_env: str = "demo"
    ctrader_account_id: str = ""
    ctrader_access_token: str = ""
    ctrader_refresh_token: str = ""
    ctrader_api_host: str = ""
    symbol: str = "XAUUSD"

    trading_enabled: bool = True
    risk_pct_default: float = 0.10
    max_concurrent_positions: int = 1
    signal_ttl_minutes: int = 180
    swing_l: int = 2
    trend_n: int = 2
    sweep_swing_lookback: int = 3
    sweep_max_age_candles: int = 50
    fvg_must_be_after_sweep: bool = True
    allow_late_entry: bool = False

    sl_buffer_points: int = 10
    min_sl_distance_points: int = 50
    max_spread_points: int = 50
    pinbar_wick_ratio: float = 2.0
    pinbar_body_ratio: float = 0.4
    strong_close_zone_pct: float = 0.2

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
