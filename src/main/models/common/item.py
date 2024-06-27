from src.main.models.common.types import Number
from src.main.models.common.dimension import Dimension


class Item:
    def __init__(self, dimension: Dimension, time: Number):
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
