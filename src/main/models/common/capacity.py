from src.main.models.common.dimension import Dimension


class Capacity:
    def __init__(self, dimension: Dimension) -> None:
        self._dimension = dimension

    @property
    def dimension(self) -> Dimension:
        return self._dimension

    @staticmethod
    def empty() -> 'Capacity':
        return Capacity(Dimension.empty())

    def fits(self, dimensions: Dimension) -> bool:
        return self._dimension > dimensions
