from src.main.models.commons.dimension import Dimension
from src.main.models.commons.types import Number


class Item:
    def __init__(self, dimension: Dimension, time: Number) -> None:
        self._dimension = dimension
        self._time = time

    @property
    def dimension(self) -> Dimension:
        return self._dimension

    @property
    def time(self) -> Number:
        return self._time

    @staticmethod
    def empty() -> 'Item':
        return Item(Dimension.empty(), 0)
