from abc import ABC, abstractmethod
from typing import List

from src.main.base.types import Coordinates, Number


class Map(ABC):

    def __init__(self, size):
        self.size = size

    @abstractmethod
    def distance(self, coord1: Coordinates, coord2: Coordinates) -> Number:
        pass

    @abstractmethod
    def acc_distance(self, coordinates: List[Coordinates]) -> Number:
        pass

    @abstractmethod
    def estimated_time(self, coord1: Coordinates, coord2: Coordinates, rate: Number) -> Number:
        pass

    @abstractmethod
    def random_point(self) -> Coordinates:
        pass

    @abstractmethod
    def move(self, origin: Coordinates, destination: Coordinates, rate: Number) -> Coordinates:
        pass
