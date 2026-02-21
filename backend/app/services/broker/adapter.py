from abc import ABC, abstractmethod


class BrokerAdapter(ABC):
    @abstractmethod
    def fetch_candles(self, symbol: str, timeframe: str, limit: int) -> list[dict]: ...

    @abstractmethod
    def get_symbol_info(self, symbol: str) -> dict: ...

    @abstractmethod
    def place_stop_order(self, **kwargs) -> dict: ...

    @abstractmethod
    def get_account_state(self) -> dict: ...
