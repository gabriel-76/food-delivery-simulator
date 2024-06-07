import uuid
from functools import reduce

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.order.order import Order
from src.main.trip.route import Route, RouteType


class Trip:
    def __init__(self, environment: FoodDeliveryEnvironment, routes: [Route]):
        self.tripe_id = uuid.uuid4()
        self.environment = environment
        self.routes = routes
        self.required_capacity = self.calculate_required_capacity()
        self.distance = self.calculate_total_distance()

    def calculate_required_capacity(self):
        dimensions = Dimensions(0, 0, 0, 0)
        for route in self.routes:
            dimensions += route.required_capacity
        return dimensions

    def has_next_route(self):
        return len(self.routes) > 0

    def next_route(self):
        self.required_capacity = self.calculate_required_capacity()
        self.distance = self.calculate_total_distance()
        return self.routes.pop(0)

    def calculate_total_distance(self):
        distance = 0

        if len(self.routes) <= 1:
            return distance

        previous_route = self.routes[0]
        for route in self.routes[1:]:
            distance += self.environment.map.distance(previous_route.coordinates, route.coordinates)
            previous_route = route

        return distance

        # for i in range(1, len(self.routes)):
        #     acc += self.environment.map.distance(self.routes[i - 1].coordinates, self.routes[i].coordinates)
        # return acc

    def extend_trip(self, other_trip):
        self.routes += other_trip.routes
        self.required_capacity = self.calculate_required_capacity()
        self.distance = self.calculate_total_distance()
