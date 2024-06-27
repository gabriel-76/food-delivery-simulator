from abc import ABC


class Available(ABC):
    def __init__(self, available: bool) -> None:
        self._available = available

    @property
    def available(self) -> bool:
        return self._available

    def enable(self) -> None:
        self._available = True

    def disable(self) -> None:
        self._available = False
