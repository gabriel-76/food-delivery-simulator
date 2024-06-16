from src.main.coast.cost_function import CostFunction
from src.main.driver.driver import Driver
from src.main.map.map import Map
from src.main.order.order_status import OrderStatus
from src.main.trip.route import Route
from src.main.trip.route_type import RouteType


class SimpleCostFunction(CostFunction):
    def __init__(self):
        self.WEIGHT_DELAY = 1
        self.WEIGHT_DISTANCE = 1
        self.MAX_PENALTY = float('inf')

    def penalty(self, route: Route):
        if route.route_type is RouteType.COLLECT and route.order.status <= OrderStatus.DRIVER_ACCEPTED:
            return 0
        if route.route_type is RouteType.DELIVERY and route.order.status <= OrderStatus.COLLECTED:
            return 0
        return self.MAX_PENALTY

    def delay(self, map: Map, driver: Driver, route: Route):
        current_delay = 0
        if driver.current_route is not None:
            current_delay = map.estimated_time(
                driver.coordinates,
                driver.current_route.coordinates,
                driver.movement_rate
            )
        new_route_delay = map.estimated_time(
            driver.coordinates,
            route.coordinates,
            driver.movement_rate
        )
        return current_delay + new_route_delay

    def distance(self, map: Map, driver: Driver, route: Route):
        current_distance = 0
        if driver.current_route is not None:
            current_distance = map.distance(
                driver.coordinates,
                driver.current_route.coordinates
            )
        new_route_distance = map.distance(
            driver.coordinates,
            route.coordinates
        )
        return current_distance + new_route_distance

    def cost(self, map: Map, driver: Driver, route: Route):
        value = (
                self.WEIGHT_DELAY * self.delay(map, driver, route) +
                self.WEIGHT_DISTANCE * self.distance(map, driver, route) +
                self.penalty(route)
        )
        # print(f"Cost: {value}")
        return value
