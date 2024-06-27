from src.main.models.order.order import Order
from src.main.models.route.segment import Segment
from src.main.models.route.segment.segment_type import SegmentType


class PickupSegment(Segment):
    def __init__(self, order: Order):
        super().__init__(SegmentType.PICKUP, order)
