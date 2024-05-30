import random
import uuid
from enum import Enum, auto

from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.base.dimensions import Dimensions
from src.driver.capacity import Capacity
from src.events.driver_accepted_delivery import DriverAcceptedDelivery
from src.events.driver_arrived_delivery_location import DriverArrivedDeliveryLocation
from src.events.driver_collected_order import DriverCollectedOrder
from src.events.driver_collecting_order import DriverCollectingOrder
from src.events.driver_delivered_order import DriverDeliveredOrder
from src.events.driver_delivering_order import DriverDeliveringOrder
from src.events.driver_rejected_delivery import DriverRejectedDelivery
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

    def deliver_order(self, order):
        yield self.environment.timeout(1)
        if self.accept_order_condition(order):
            self.accept_delivery(order)
        else:
            self.reject_delivery(order)

    def accept_delivery(self, order: Order):
        event = DriverAcceptedDelivery(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        self.environment.process(self.start_order_collection(order))

    def reject_delivery(self, order: Order):
        event = DriverRejectedDelivery(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        self.environment.add_rejected_delivery_order(order)

    def start_order_collection(self, order):
        self.status = DriverStatus.COLLECTING
        collecting_time = self.collecting_time_policy()
        event = DriverCollectingOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        yield self.environment.timeout(collecting_time)
        self.finish_order_collection(order)

    def finish_order_collection(self, order):
        event = DriverCollectedOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        self.environment.process(self.start_order_delivery(order))

    def start_order_delivery(self, order: Order):
        self.status = DriverStatus.DELIVERING
        delivery_time = self.delivery_time_policy()
        event = DriverDeliveringOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        yield self.environment.timeout(delivery_time)
        self.environment.process(self.wait_client_pick_up_order(order))

    def wait_client_pick_up_order(self, order: Order):
        event = DriverArrivedDeliveryLocation(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        yield self.environment.process(order.client.receive_order(order, self))
        self.finish_order_delivery(order)

    def finish_order_delivery(self, order: Order):
        event = DriverDeliveredOrder(
            order_id=order.order_id,
            client_id=order.client.client_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=self.driver_id,
            time=self.environment.now
        )
        self.environment.add_event(event)
        self.status = DriverStatus.WAITING
        self.environment.add_delivered_order(order)

    def delivery_time_policy(self):
        return random.randrange(1, 5)

    def collecting_time_policy(self):
        return random.randrange(1, 5)

    def accept_order_condition(self, order):
        return self.available and self.status is DriverStatus.WAITING


class DriverStatus(Enum):
    WAITING = auto()
    COLLECTING = auto()
    DELIVERING = auto()
