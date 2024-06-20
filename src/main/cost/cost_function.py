from abc import ABC, abstractmethod

from src.main.actors.driver import Driver
from src.main.map.map import Map
from src.main.route.route_segment import RouteSegment


class CostFunction(ABC):

    @abstractmethod
    def cost(self, map: Map, driver: Driver, route_segment: RouteSegment):
        pass
