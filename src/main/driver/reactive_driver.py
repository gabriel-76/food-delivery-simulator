import random

from src.main.driver.capacity import Capacity
from src.main.driver.driver import Driver, DriverStatus
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment


class ReactiveDriver(Driver):
    def __init__(
            self,
            environment: FoodDeliveryEnvironment,
            coordinates, capacity: Capacity,
            available: bool,
            status: DriverStatus,
            movement_rate
    ):
        super().__init__(environment, coordinates, capacity, available, status, movement_rate)
        self.environment.process(self.search_order())

    def accept_order_condition(self, order):
        default_condition = super().accept_order_condition(order)
        collection_coordinate = self.environment.map.distance(self.coordinates, order.restaurant.coordinates)
        return default_condition and collection_coordinate <= random.randrange(5, 100)

    def search_order(self):
        while True:
            search_timeout = self.environment.timeout(15)
            order_request = self.environment.ready_orders.get(self.accept_order_condition)
            search_result = yield self.environment.any_of([order_request, search_timeout])
            if order_request in search_result:
                self.accept_delivery(order_request.value)
            yield self.environment.timeout(3)
