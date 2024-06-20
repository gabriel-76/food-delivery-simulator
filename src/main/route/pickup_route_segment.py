from src.main.order.order import Order
from src.main.route.route_segment import RouteSegment
from src.main.route.route_segment_type import RouteSegmentType


class PickupRouteSegment(RouteSegment):
    def __init__(self, order: Order):
        super().__init__(RouteSegmentType.PICKUP, order)
