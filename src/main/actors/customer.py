import random
import uuid

from simpy.events import ProcessGenerator

from src.main.actors.map_actor import MapActor
from src.main.actors.restaurant import Restaurant
from src.main.base.types import Coordinates
from src.main.actors.driver import Driver
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.events.customer_placed_order import CustomerPlacedOrder
from src.main.events.customer_received_order import CustomerReceivedOrder
from src.main.order.order import Order
from src.main.order.order_status import OrderStatus


class Customer(MapActor):
    def __init__(self, environment: FoodDeliverySimpyEnv, coordinates: Coordinates, available: bool) -> None:
        self.customer_id = uuid.uuid4()
        super().__init__(environment, coordinates, available)

    def place_order(self, order: Order, restaurant: Restaurant) -> None:
        self.publish_event(CustomerPlacedOrder(
            order_id=order.order_id,
            customer_id=self.customer_id,
            restaurant_id=restaurant.restaurant_id,
            time=self.now
        ))
        restaurant.receive_order_requests([order])
        order.update_status(OrderStatus.PLACED)

    def receive_order(self, order: Order, driver: Driver) -> ProcessGenerator:
        yield self.timeout(self.time_to_receive_order(order))
        self.publish_event(CustomerReceivedOrder(
            order_id=order.order_id,
            customer_id=self.customer_id,
            restaurant_id=order.restaurant.restaurant_id,
            driver_id=driver.driver_id,
            time=self.now
        ))
        order.update_status(OrderStatus.RECEIVED)

    def time_to_receive_order(self, order: Order):
        return random.randrange(2, 10)

