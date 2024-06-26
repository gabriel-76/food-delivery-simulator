from typing import List

from src.main.customer.customer import Customer
from src.main.driver.driver import Driver
from src.main.order.order import Order


class DeliveryEnvState:
    def __init__(self):
        self._customers: List[Customer] = []
        self._establishments = []
        self._drivers: List[Driver] = []
        self._orders: List[Order] = []

        # Orders ready for picking up
        self.orders_awaiting_delivery: List[Order] = []

        self.events = []

    @property
    def customers(self) -> List[Customer]:
        return self._customers

    @property
    def establishments(self) -> List:
        return self._establishments

    @property
    def drivers(self) -> List:
        return self._drivers

    @property
    def orders(self) -> List[Order]:
        return self._orders

    def add_customers(self, customer: List[Customer]):
        self._customers += customer

    def add_establishments(self, establishments: List) -> None:
        self._establishments += establishments

    def add_drivers(self, drivers: List) -> None:
        self._drivers += drivers

    def add_orders(self, orders: List) -> None:
        self._orders += orders

    def add_event(self, event) -> None:
        self.events.append(event)

    def log_events(self) -> None:
        for event in self.events:
            print(event)
