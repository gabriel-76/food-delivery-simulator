import random
from enum import Enum, auto

from src.environment.food_delivery_environment import FoodDeliveryEnvironment
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
            capacity: Capacity,
            available: bool,
            status
    ):
        self.environment = environment
        self.name = name
        self.coordinates = coordinates
        self.driver_type = driver_type
        self.capacity = capacity
        self.available = available

    def fits(self, order: Order):
        dimensions = Dimensions(0, 0, 0, 0)
        for item in order.items:
            dimensions += item.dimensions
        return self.capacity.fits(dimensions)

    def collect_order(self, order):
        collecting_time = self.collecting_time_policy()
        print(f"Driver {self.name} collecting order_{order.order_id} from {order.restaurant.name} to {order.client.name} in {collecting_time}")
        yield self.environment.timeout(collecting_time)

    def deliver_order(self, order: Order):
        self.environment.process(self.collect_order(order))
        delivery_time = self.delivery_time_policy()
        yield self.environment.timeout(delivery_time)
        print(f"Driver {self.name} delivered order_{order.order_id} from {order.restaurant.name} to {order.client.name} in {delivery_time}")


    def delivery_time_policy(self):
        return random.randrange(1, 5)

    def collecting_time_policy(self):
        return random.randrange(1, 5)

    def accept_order(self, order):
        return self.available


class DriverStatus(Enum):
    WAITING = auto()
    COLLECTING = auto()
    DELIVERING = auto()