from src.main.models.order.order import Order
from src.main.models.route.segment.segment import Segment
from src.main.models.route.segment.segment_type import SegmentType


class DeliverySegment(Segment):
    def __init__(self, order: Order):
        super().__init__(order, SegmentType.DELIVERY)
