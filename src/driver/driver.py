import random

from src import FoodDeliveryEnvironment
from src.base.dimensions import Dimensions
from src.driver.capacity import Capacity
from src.order.order import Order


class Driver:
    def __init__(
            self,
            environment: FoodDeliveryEnvironment,
            name,
            coordinates,
            driver_type,
            capacity: Capacity
    ):
        self.environment = environment
        self.name = name
        self.coordinates = coordinates
        self.driver_type = driver_type
        self.capacity = capacity

    def fits(self, order: Order):
        dimensions = Dimensions(0, 0, 0, 0)
        for item in order.items:
            dimensions += item.dimensions
        return self.capacity.fits(dimensions)

    def deliver_order(self, order: Order):
        delivery_time = self.delivery_time_policy()
        yield self.environment.timeout(delivery_time)
        print(f"Driver {self.name} delivered order_{order.order_id} from {order.restaurant.name} to {order.client.name} in {delivery_time}")

    def delivery_time_policy(self):
        return random.randrange(1, 5)
