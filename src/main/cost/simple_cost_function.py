from src.main.models.base import Number
from src.main.cost.cost_function import CostFunction
from src.main.models.driver import Driver
from src.main.map.map import Map
from src.main.models.order import OrderStatus
from src.main.models.route.segment import Segment


class SimpleCostFunction(CostFunction):
    def __init__(self):
        self.WEIGHT_DELAY = 1
        self.WEIGHT_DISTANCE = 1
        self.MAX_PENALTY = float('inf')

    def penalty(self, route_segment: Segment):
        if route_segment.is_pickup() and route_segment._order._status <= OrderStatus.DRIVER_ACCEPTED:
            return 0
        if route_segment.is_delivery() and route_segment._order._status <= OrderStatus.PICKED_UP:
            return 0
        return self.MAX_PENALTY

    def delay(self, map: Map, driver: Driver, route_segment: Segment):
        current_delay = 0
        if driver._segment is not None:
            current_delay = map.estimated_time(
                driver.coordinate,
                driver._segment._coordinate,
                driver._movement_rate
            )
        new_segment_delay = map.estimated_time(
            driver.coordinate,
            route_segment._coordinate,
            driver._movement_rate
        )
        return current_delay + new_segment_delay

    def distance(self, map: Map, driver: Driver, route_segment: Segment):
        current_distance = 0
        if driver._segment is not None:
            current_distance = map.distance(
                driver.coordinate,
                driver._segment._coordinate
            )
        new_segment_distance = map.distance(
            driver.coordinate,
            route_segment._coordinate
        )
        return current_distance + new_segment_distance

    def cost(self, map: Map, driver: Driver, route_segment: Segment) -> Number:
        value = (
                self.WEIGHT_DELAY * self.delay(map, driver, route_segment) +
                self.WEIGHT_DISTANCE * self.distance(map, driver, route_segment) +
                self.penalty(route_segment)
        )
        # print(f"Cost: {value}")
        return value
