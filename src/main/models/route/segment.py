from enum import Enum, auto

from src.main.models.commons.types import Coordinate, Number
from src.main.models.order.order import Order


class SegmentType(Enum):
    PICKUP = auto()
    DELIVERY = auto()


class Segment:
    def __init__(self, order: Order, segment_type: SegmentType):
        self._order = order
        self._segment_type = segment_type
        self._coordinate: Coordinate = self.extract_coordinate()
        self._dimension = self._order.dimension

    @property
    def order(self) -> Order:
        return self._order

    @property
    def coordinate(self):
        return self._coordinate

    @property
    def dimension(self):
        return self._dimension

    def accept_pickup(self, time: Number, estimated_time: Number):
        self._order.accept_pickup(time, estimated_time)

    def is_ready(self) -> bool:
        return self._order.is_ready()

    def extract_coordinate(self):
        if self.is_pickup():
            return self._order.establishment.coordinate
        return self._order.customer.coordinate

    def is_pickup(self) -> bool:
        return self._segment_type == SegmentType.PICKUP

    def is_delivery(self) -> bool:
        return self._segment_type == SegmentType.DELIVERY


class PickupSegment(Segment):
    def __init__(self, order: Order):
        super().__init__(order, SegmentType.PICKUP)


class DeliverySegment(Segment):
    def __init__(self, order: Order):
        super().__init__(order, SegmentType.DELIVERY)
