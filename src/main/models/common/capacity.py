from src.main.models.common.dimension import Dimension
from src.main.models.common.types import Number


class Capacity:
    def __init__(self, dimension: Dimension) -> None:
        self._dimension = dimension

    @property
    def dimension(self) -> Dimension:
        return self._dimension

    @property
    def value(self) -> Number:
        return self._dimension.volume * self._dimension.weight

    @staticmethod
    def empty() -> 'Capacity':
        return Capacity(Dimension.empty())

    def fits(self, dimension: Dimension) -> bool:
        return self._dimension > dimension
