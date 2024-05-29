import random
import uuid
from enum import Enum, auto

from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.base.dimensions import Dimensions
from src.driver.capacity import Capacity
from src.order.order import Order


class Driver:
    def __init__(
            self,
            environment: FoodDeliveryEnvironment,
            coordinates,
            driver_type,
            capacity: Capacity,
            available: bool,
            status
    ):
        self.driver_id = uuid.uuid4()
        self.environment = environment
        self.coordinates = coordinates
        self.driver_type = driver_type
        self.capacity = capacity
        self.available = available
        self.status = status

    def fits(self, order: Order):
        dimensions = Dimensions(0, 0, 0, 0)
        for item in order.items:
            dimensions += item.dimensions
        return self.capacity.fits(dimensions)

    def deliver(self, order):
        if self.accept_order(order):
            print(f"Driver {self.driver_id} accepted order {order.order_id} from {order.restaurant.restaurant_id} and client {order.client.client_id}")
            self.environment.process(self.collect_order(order))
        else:
            print(f"Driver {self.driver_id} reject order {order.order_id} from {order.restaurant.restaurant_id} and client {order.client.client_id}")
            self.environment.add_rejected_delivery_order(order)
        yield self.environment.timeout(1)

    def collect_order(self, order):
        self.status = DriverStatus.COLLECTING
        collecting_time = self.collecting_time_policy()
        print(f"Driver {self.driver_id} collecting order {order.order_id} from {order.restaurant.restaurant_id} to {order.client.client_id} in {collecting_time}")
        yield self.environment.timeout(collecting_time)
        self.environment.process(self.deliver_order(order))

    def deliver_order(self, order: Order):
        self.status = DriverStatus.DELIVERING
        delivery_time = self.delivery_time_policy()
        yield self.environment.timeout(delivery_time)
        print(f"Driver {self.driver_id} delivered order {order.order_id} from {order.restaurant.restaurant_id} to {order.client.client_id} in {delivery_time}")
        self.status = DriverStatus.WAITING
        self.environment.add_delivered_order(order)


    def delivery_time_policy(self):
        return random.randrange(1, 5)

    def collecting_time_policy(self):
        return random.randrange(1, 5)

    def accept_order(self, order):
        return self.available and self.status is DriverStatus.WAITING


class DriverStatus(Enum):
    WAITING = auto()
    COLLECTING = auto()
    DELIVERING = auto()
