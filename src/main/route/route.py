import uuid
from typing import List

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.route.route_segment import RouteSegment


class Route:
    def __init__(self, environment: FoodDeliverySimpyEnv, route_segments: List[RouteSegment]):
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

    def has_next(self):
        return len(self.route_segments) > 0

    def next(self):
        self.required_capacity = self.calculate_required_capacity()
        self.distance = self.calculate_total_distance()
        return self.route_segments.pop(0)

    def calculate_total_distance(self):
        coordinates = [segment.coordinate for segment in self.route_segments]
        return self.environment.map.acc_distance(coordinates)

    def extend_route(self, other_route):
        self.route_segments += other_route.route_segments
        self.required_capacity = self.calculate_required_capacity()
        self.distance = self.calculate_total_distance()

    def size(self):
        return len(self.route_segments)
