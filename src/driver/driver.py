import random

from simpy import Environment
from src.driver.capacity import Capacity
from src.order.order import Order


class Driver:
    def __init__(
            self,
            environment: Environment,
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

    def deliver_order(self, order: Order):
        delivery_time = self.delivery_time()
        yield self.environment.timeout(delivery_time)
        print(f"Driver {self.name} delivered from {order.restaurant.name} to {order.client.name} in {delivery_time}")


    def delivery_time(self):
        return random.randrange(1, 20)
