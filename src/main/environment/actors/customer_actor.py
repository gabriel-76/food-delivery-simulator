import random
from typing import TYPE_CHECKING

from simpy.core import SimTime
from simpy.events import ProcessGenerator

from src.main.environment.actors.actor import Actor
from src.main.events.customer_placed_order import CustomerPlacedOrder
from src.main.events.customer_received_order import CustomerReceivedOrder
from src.main.models.customer.customer import Customer
from src.main.models.driver.driver import Driver
from src.main.models.establishment.establishment import Establishment
from src.main.models.order.order import Order

if TYPE_CHECKING:
    from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv


class CustomerActor(Actor):
    def __init__(self, environment: 'FoodDeliverySimpyEnv', customer: Customer) -> None:
        super().__init__(environment)
        self._customer = customer

    def place(self, order: Order, establishment: Establishment) -> None:
        self._customer.place(order, establishment, self.now)
        self.publish_event(CustomerPlacedOrder(
            order_id=order.identifier,
            customer_id=self._customer.identifier,
            establishment_id=establishment.identifier,
            time=self.now
        ))

    def receive(self, order: Order, driver: Driver) -> ProcessGenerator:
        yield self.timeout(self.receive_time(order))
        self._customer.receive(order, driver, self.now)
        self.publish_event(CustomerReceivedOrder(
            order_id=order.identifier,
            customer_id=self._customer.identifier,
            establishment_id=order.establishment.identifier,
            driver_id=driver.identifier,
            time=self.now
        ))

    def receive_time(self, order: Order) -> SimTime:
        return random.randrange(2, 10)
