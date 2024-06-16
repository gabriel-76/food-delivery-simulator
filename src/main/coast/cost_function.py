from abc import ABC, abstractmethod

from src.main.driver.driver import Driver
from src.main.map.map import Map
from src.main.trip.route import Route


class CostFunction(ABC):

    @abstractmethod
    def cost(self, map: Map, driver: Driver, route: Route):
        pass
