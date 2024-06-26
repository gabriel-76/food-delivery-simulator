from src.main.order.order import Order
from src.main.route.route_segment_type import RouteSegmentType


class RouteSegment:
    def __init__(self, route_segment_type: RouteSegmentType, order: Order):
        self.route_segment_type = route_segment_type
        self.order = order
        self.coordinates = self.init_coordinates()
        self.required_capacity = self.order.required_capacity

    def init_coordinates(self):
        if self.is_pickup():
            return self.order.establishment.coordinates
        return self.order.customer.coordinates

    def is_pickup(self) -> bool:
        return self.route_segment_type == RouteSegmentType.PICKUP

    def is_delivery(self) -> bool:
        return self.route_segment_type == RouteSegmentType.DELIVERY
