from abc import ABC, abstractmethod

from src.main.base.types import Number
from src.main.driver.driver import Driver
from src.main.map.map import Map
from src.main.route.route_segment import RouteSegment


class CostFunction(ABC):

    @abstractmethod
    def cost(self, map: Map, driver: Driver, route_segment: RouteSegment) -> Number:
        pass
