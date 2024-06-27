from src.main.models.common.types import Coordinate
from src.main.models.order.order import Order
from src.main.models.route.segment.segment_type import SegmentType


class Segment:
    def __init__(self, order: Order, segment_type: SegmentType):
        self._order = order
        self._segment_type = segment_type
        self._coordinate: Coordinate = self.extract_coordinate()
        self._dimension = self._order.dimension

    def extract_coordinate(self):
        if self.is_pickup():
            return self._order.establishment.coordinate
        return self._order.customer.coordinate

    def is_pickup(self) -> bool:
        return self._segment_type == SegmentType.PICKUP

    def is_delivery(self) -> bool:
        return self._segment_type == SegmentType.DELIVERY
