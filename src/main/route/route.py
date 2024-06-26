import uuid
from typing import List

from src.main.base.dimensions import Dimensions
from src.main.route.route_segment import RouteSegment


class Route:
    def __init__(self, route_segments: List[RouteSegment]):
        self.route_id = uuid.uuid4()
        self.route_segments = route_segments
        self.required_capacity = self.calculate_required_capacity()

    @property
    def coordinates(self):
        return [segment.coordinate for segment in self.route_segments]

    def calculate_required_capacity(self):
        dimensions = Dimensions(0, 0, 0, 0)
        for route_segment in self.route_segments:
            dimensions += route_segment.required_capacity
        return dimensions

    def has_next(self):
        return len(self.route_segments) > 0

    def next(self):
        self.required_capacity = self.calculate_required_capacity()
        return self.route_segments.pop(0)

    def extend_route(self, other_route):
        self.route_segments += other_route.route_segments
        self.required_capacity = self.calculate_required_capacity()

    def size(self):
        return len(self.route_segments)
