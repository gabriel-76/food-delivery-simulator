from abc import ABC, abstractmethod

from src.main.driver.driver import Driver
from src.main.map.map import Map
from src.main.route.segment import Segment


class CostFunction(ABC):

    @abstractmethod
    def cost(self, map: Map, driver: Driver, segment: Segment):
        pass
