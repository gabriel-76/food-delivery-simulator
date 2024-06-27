from abc import ABC, abstractmethod
from typing import List

from src.main.base.types import Coordinate, Number


class Map(ABC):

    def __init__(self, size):
        self.size = size

    @abstractmethod
    def distance(self, coord1: Coordinate, coord2: Coordinate) -> Number:
        pass

    @abstractmethod
    def acc_distance(self, coordinates: List[Coordinate]) -> Number:
        pass

    @abstractmethod
    def estimated_time(self, coord1: Coordinate, coord2: Coordinate, rate: Number) -> Number:
        pass

    @abstractmethod
    def random_point(self) -> Coordinate:
        pass

    @abstractmethod
    def move(self, origin: Coordinate, destination: Coordinate, rate: Number) -> Coordinate:
        pass
