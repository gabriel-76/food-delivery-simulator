from abc import ABC, abstractmethod

from src.main.commons.types import Number
from src.main.map.map import Map
from src.main.models.driver.driver import Driver
from src.main.models.route.segment import Segment


class CostFunction(ABC):

    @abstractmethod
    def cost(self, map: Map, driver: Driver, route_segment: Segment) -> Number:
        pass
