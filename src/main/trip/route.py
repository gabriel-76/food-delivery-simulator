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
        self.required_capacity = self.order.required_capacity

