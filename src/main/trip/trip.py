import uuid
from functools import reduce

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.order.order import Order
from src.main.trip.route import Route, RouteType


class Trip:
    def __init__(self, environment: FoodDeliveryEnvironment, routes: [Route]):
        self.order_id = uuid.uuid4()
        self.environment = environment
        self.routes = routes
        self.required_capacity = self.calculate_required_capacity()
        # self.distance = self.calculate_total_distance()

    def calculate_required_capacity(self):
        dimensions = Dimensions(0, 0, 0, 0)
        for route in self.routes:
            dimensions += route.required_capacity
        return dimensions

    def has_next_route(self):
        return len(self.routes) > 0

    def next_route(self):
        return self.routes.pop(0)

    # def distance_rule(self, route1: Route, route2: Route):
    #     restaurant1_coords = route1.order.restaurant.coordinates
    #     restaurant2_coords = route2.order.restaurant.coordinates
    #     client1_coords = route1.order.client.coordinates
    #     client2_coords = route2.order.client.coordinates
    #
    #     if route1.route_type is RouteType.COLLECT and route2.route_type is RouteType.COLLECT:
    #         return self.environment.map.distance(restaurant1_coords, restaurant2_coords)
    #
    #     if route1.route_type is RouteType.COLLECT and route2.route_type is RouteType.DELIVERY:
    #         return self.environment.map.distance(restaurant1_coords, client2_coords)
    #
    #     if route1.route_type is RouteType.DELIVERY and route2.route_type is RouteType.COLLECT:
    #         return self.environment.map.distance(client1_coords, restaurant2_coords)
    #
    #     if route1.route_type is RouteType.DELIVERY and route2.route_type is RouteType.DELIVERY:
    #         return self.environment.map.distance(client1_coords, client2_coords)
    #
    # def calculate_total_distance(self):
    #     return reduce(lambda route1, route2: self.distance_rule(route1, route2), self.routes)

    def extend_trip(self, other_trip):
        self.routes += other_trip.routes
