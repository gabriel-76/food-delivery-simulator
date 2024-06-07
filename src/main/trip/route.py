from enum import Enum, auto

from src.main.base.dimensions import Dimensions
from src.main.order.order import Order


class RouteType(Enum):
    COLLECT = auto()
    DELIVERY = auto()


class Route:
    def __init__(self, route_type: RouteType, order: Order):
        self.route_type = route_type
        self.order = order
        self.coordinates = self.init_coordinates()
        self.required_capacity = self.order.required_capacity

    def init_coordinates(self):
        if self.route_type is RouteType.COLLECT:
            return self.order.restaurant.coordinates
        if self.route_type is RouteType.DELIVERY:
            return self.order.client.coordinates

