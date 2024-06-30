import uuid
from typing import List

from src.main.commons.types import Coordinate, Number
from src.main.models.commons.dimension import Dimension
from src.main.models.route.segment import Segment


class Route:
    def __init__(self, segments: List[Segment]):
        self.route_id = uuid.uuid4()
        self._segments = segments
        self._dimension: Dimension = self._calculate_dimension()

    @property
    def coordinates(self) -> List[Coordinate]:
        return [segment.coordinate for segment in self._segments]

    @property
    def segments(self) -> List[Segment]:
        return self._segments

    def get_segment(self) -> Segment:
        return self._segments.pop(0)

    @property
    def dimension(self) -> Dimension:
        return self._dimension

    @property
    def size(self) -> int:
        return len(self._segments)

    def accept_pickup(self, time: Number, estimated_time: Number):
        for segment in self._segments:
            segment.order.accept_pickup(time, estimated_time)

    def _calculate_dimension(self) -> Dimension:
        dimension = Dimension.empty()
        for segment in self._segments:
            dimension += segment.dimension
        return dimension

    def extend(self, route: 'Route'):
        self._dimension += route.dimension
        self._segments += route.segments

    @staticmethod
    def empty():
        return Route([])
