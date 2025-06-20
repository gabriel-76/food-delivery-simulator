import random
import uuid

from simpy.events import ProcessGenerator

from src.main.actors.map_actor import MapActor
from src.main.base.types import Coordinate
from src.main.driver.driver import Driver
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.events.customer_placed_order import CustomerPlacedOrder
from src.main.events.customer_received_order import CustomerReceivedOrder
from src.main.order.order import Order
from src.main.order.order_status import OrderStatus
from src.main.establishment.establishment import Establishment


class Customer(MapActor):
    def __init__(self, environment: FoodDeliverySimpyEnv, coordinate: Coordinate, available: bool) -> None:
        self.customer_id = uuid.uuid4()
        super().__init__(environment, coordinate, available)

    def place_order(self, order: Order, establishment: Establishment) -> None:
        self.publish_event(CustomerPlacedOrder(
            order_id=order.order_id,
            customer_id=self.customer_id,
            establishment_id=establishment.establishment_id,
            time=self.now
        ))
        establishment.receive_order_requests([order])
        order.update_status(OrderStatus.PLACED)

    def receive_order(self, order: Order, driver: Driver) -> ProcessGenerator:
        yield self.timeout(self.time_to_receive_order(order))
        self.publish_event(CustomerReceivedOrder(
            order_id=order.order_id,
            customer_id=self.customer_id,
            establishment_id=order.establishment.establishment_id,
            driver_id=driver.driver_id,
            time=self.now
        ))
        order.update_status(OrderStatus.RECEIVED)

    def time_to_receive_order(self, order: Order):
        return random.randrange(2, 10)

