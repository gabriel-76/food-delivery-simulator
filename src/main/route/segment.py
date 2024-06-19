from src.main.order.order import Order
from src.main.route.segment_type import SegmentType


class Segment:
    def __init__(self, segment_type: SegmentType, order: Order):
        self.segment_type = segment_type
        self.order = order
        self.coordinates = self.init_coordinates()
        self.required_capacity = self.order.required_capacity

    def init_coordinates(self):
        if self.segment_type is SegmentType.PICKUP:
            return self.order.restaurant.coordinates
        if self.segment_type is SegmentType.DELIVERY:
            return self.order.client.coordinates
