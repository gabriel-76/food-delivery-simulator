from abc import ABC

from src.main.models.base.types import Coordinate


class Localizable(ABC):
    def __init__(self, coordinate: Coordinate) -> None:
        self._coordinate = coordinate

    @property
    def coordinate(self) -> Coordinate:
        return self._coordinate
