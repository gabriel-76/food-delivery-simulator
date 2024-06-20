from src.main.order.order import Order
from src.main.route.route_segment_type import RouteSegmentType


class RouteSegment:
    def __init__(self, route_segment_type: RouteSegmentType, order: Order):
        self.route_segment_type = route_segment_type
        self.order = order
        self.coordinates = self.init_coordinates()
        self.required_capacity = self.order.required_capacity

    def init_coordinates(self):
        if self.route_segment_type is RouteSegmentType.PICKUP:
            return self.order.restaurant.coordinates
        if self.route_segment_type is RouteSegmentType.DELIVERY:
            return self.order.client.coordinates
