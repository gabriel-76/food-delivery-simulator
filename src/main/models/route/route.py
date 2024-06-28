import uuid
from typing import List

from src.main.models.commons.dimension import Dimension
from src.main.models.commons.types import Coordinate
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

    @property
    def dimension(self) -> Dimension:
        return self._dimension

    @property
    def size(self) -> int:
        return len(self._segments)

    def _calculate_dimension(self) -> Dimension:
        dimension = Dimension.empty()
        for segment in self._segments:
            dimension += segment.dimension
        return dimension

    def has_next(self):
        return len(self._segments) > 0

    def next(self):
        return self._segments.pop(0)

    def extend_route(self, route: 'Route'):
        self._dimension += route.dimension
        self._segments += route.segments
