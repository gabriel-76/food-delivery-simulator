from src.main.base.types import Number
from src.main.cost.cost_function import CostFunction
from src.main.driver.driver_actor import DriverActor
from src.main.map.map import Map
from src.main.order.order_status import OrderStatus
from src.main.route.route_segment import RouteSegment


class SimpleCostFunction(CostFunction):
    def __init__(self):
        self.WEIGHT_DELAY = 1
        self.WEIGHT_DISTANCE = 1
        self.MAX_PENALTY = float('inf')

    def penalty(self, route_segment: RouteSegment):
        if route_segment.is_pickup() and route_segment.order.status <= OrderStatus.DRIVER_ACCEPTED:
            return 0
        if route_segment.is_delivery() and route_segment.order.status <= OrderStatus.PICKED_UP:
            return 0
        return self.MAX_PENALTY

    def delay(self, map: Map, driver: DriverActor, route_segment: RouteSegment):
        current_delay = 0
        if driver.current_route_segment is not None:
            current_delay = map.estimated_time(
                driver.coordinate,
                driver.current_route_segment.coordinate,
                driver.movement_rate
            )
        new_segment_delay = map.estimated_time(
            driver.coordinate,
            route_segment.coordinate,
            driver.movement_rate
        )
        return current_delay + new_segment_delay

    def distance(self, map: Map, driver: DriverActor, route_segment: RouteSegment):
        current_distance = 0
        if driver.current_route_segment is not None:
            current_distance = map.distance(
                driver.coordinate,
                driver.current_route_segment.coordinate
            )
        new_segment_distance = map.distance(
            driver.coordinate,
            route_segment.coordinate
        )
        return current_distance + new_segment_distance

    def cost(self, map: Map, driver: DriverActor, route_segment: RouteSegment) -> Number:
        value = (
                self.WEIGHT_DELAY * self.delay(map, driver, route_segment) +
                self.WEIGHT_DISTANCE * self.distance(map, driver, route_segment) +
                self.penalty(route_segment)
        )
        # print(f"Cost: {value}")
        return value
