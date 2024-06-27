import uuid
from typing import List

from src.main.models.common.dimension import Dimension
from src.main.models.route.segment.segment import Segment


class Route:
    def __init__(self, segments: List[Segment]):
        self.route_id = uuid.uuid4()
        self._segments = segments
        self.dimension: Dimension = self.calculate_required_capacity()

    @property
    def coordinates(self):
        return [segment._coordinate for segment in self._segments]

    def calculate_required_capacity(self):
        dimensions = Dimension.empty()
        for route_segment in self._segments:
            dimensions += route_segment.required_capacity
        return dimensions

    def has_next(self):
        return len(self._segments) > 0

    def next(self):
        self.required_capacity = self.calculate_required_capacity()
        return self._segments.pop(0)

    def extend_route(self, other_route):
        self._segments += other_route._segments
        self.required_capacity = self.calculate_required_capacity()

    def size(self):
        return len(self._segments)
