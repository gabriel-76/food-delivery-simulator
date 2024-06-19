from src.main.coast.cost_function import CostFunction
from src.main.driver.driver import Driver
from src.main.map.map import Map
from src.main.order.order_status import OrderStatus
from src.main.route.segment import Segment
from src.main.route.segment_type import SegmentType


class SimpleCostFunction(CostFunction):
    def __init__(self):
        self.WEIGHT_DELAY = 1
        self.WEIGHT_DISTANCE = 1
        self.MAX_PENALTY = float('inf')

    def penalty(self, segment: Segment):
        if segment.segment_type is SegmentType.PICKUP and segment.order.status <= OrderStatus.DRIVER_ACCEPTED:
            return 0
        if segment.segment_type is SegmentType.DELIVERY and segment.order.status <= OrderStatus.PICKED_UP:
            return 0
        return self.MAX_PENALTY

    def delay(self, map: Map, driver: Driver, segment: Segment):
        current_delay = 0
        if driver.current_segment is not None:
            current_delay = map.estimated_time(
                driver.coordinates,
                driver.current_segment.coordinates,
                driver.movement_rate
            )
        new_segment_delay = map.estimated_time(
            driver.coordinates,
            segment.coordinates,
            driver.movement_rate
        )
        return current_delay + new_segment_delay

    def distance(self, map: Map, driver: Driver, segment: Segment):
        current_distance = 0
        if driver.current_segment is not None:
            current_distance = map.distance(
                driver.coordinates,
                driver.current_segment.coordinates
            )
        new_segment_distance = map.distance(
            driver.coordinates,
            segment.coordinates
        )
        return current_distance + new_segment_distance

    def cost(self, map: Map, driver: Driver, segment: Segment):
        value = (
                self.WEIGHT_DELAY * self.delay(map, driver, segment) +
                self.WEIGHT_DISTANCE * self.distance(map, driver, segment) +
                self.penalty(segment)
        )
        # print(f"Cost: {value}")
        return value
