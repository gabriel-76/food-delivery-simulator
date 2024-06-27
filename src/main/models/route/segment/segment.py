from src.main.models.order.order import Order
from src.main.models.route.segment.segment_type import SegmentType


class Segment:
    def __init__(self, route_segment_type: SegmentType, order: Order):
        self.route_segment_type = route_segment_type
        self.order = order
        self.coordinate = self.init_coordinates()
        self.required_capacity = self.order.required_capacity

    def init_coordinates(self):
        if self.is_pickup():
            return self.order.establishment.coordinate
        return self.order.customer.coordinate

    def is_pickup(self) -> bool:
        return self.route_segment_type == SegmentType.PICKUP

    def is_delivery(self) -> bool:
        return self.route_segment_type == SegmentType.DELIVERY
