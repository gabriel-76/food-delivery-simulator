import uuid
from functools import reduce

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.order.order import Order
from src.main.route.route_segment import RouteSegment, RouteSegmentType


class Route:
    def __init__(self, environment: FoodDeliverySimpyEnv, route_segments: [RouteSegment]):
        self.route_id = uuid.uuid4()
        self.environment = environment
        self.route_segments = route_segments
        self.required_capacity = self.calculate_required_capacity()
        self.distance = self.calculate_total_distance()

    def calculate_required_capacity(self):
        dimensions = Dimensions(0, 0, 0, 0)
        for route_segment in self.route_segments:
            dimensions += route_segment.required_capacity
        return dimensions

    def has_next_segments(self):
        return len(self.route_segments) > 0

    def next_segments(self):
        self.required_capacity = self.calculate_required_capacity()
        self.distance = self.calculate_total_distance()
        return self.route_segments.pop(0)

    def calculate_total_distance(self):
        distance = 0

        if len(self.route_segments) <= 1:
            return distance

        previous_route_segment = self.route_segments[0]
        for route_segment in self.route_segments[1:]:
            distance += self.environment.map.distance(previous_route_segment.coordinates, route_segment.coordinates)
            previous_route_segment = route_segment

        return distance

    def extend_route(self, other_route):
        self.route_segments += other_route.route_segments
        self.required_capacity = self.calculate_required_capacity()
        self.distance = self.calculate_total_distance()

    def size(self):
        return len(self.route_segments)
