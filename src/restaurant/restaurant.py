import random

import simpy

from src import FoodDeliveryEnvironment
from src.restaurant.catalog import Catalog


class Restaurant:
    def __init__(
            self,
            environment: FoodDeliveryEnvironment,
            name: str,
            coordinates,
            available: bool,
            catalog: Catalog
    ):
        self.environment = environment
        self.name = name
        self.coordinates = coordinates
        self.available = available
        self.catalog = catalog
        self.new_orders = simpy.Store(self.environment)
        self.confirmed_orders = simpy.Store(self.environment)
        self.canceled_orders = simpy.Store(self.environment)

        self.environment.process(self.accept_orders())
        self.environment.process(self.prepare_orders())

    def receive_orders(self, orders):
        for order in orders:
            self.new_orders.put(order)

    def accept_orders(self):
        while True:
            while len(self.new_orders.items) > 0:
                order = yield self.new_orders.get()
                self.environment.process(self.accept_order(order))
            yield self.environment.timeout(2)

    def accept_order(self, order):
        if self.accept_order_policy(order):
            print(f"Order order_{order.order_id} accepted")
            self.confirmed_orders.put(order)
        else:
            print(f"Order order_{order.order_id} rejected")
            self.canceled_orders.put(order)
        yield self.environment.timeout(1)

    def prepare_orders(self):
        while True:
            while len(self.confirmed_orders.items) > 0:
                order = yield self.confirmed_orders.get()
                self.environment.process(self.prepare_order(order))
            yield self.environment.timeout(2)

    def prepare_order(self, order):
        orders_time_policy = self.receiving_order_time_policy(order)
        print(
            f"The {self.name} is preparing the order {order.order_id} for the {order.client.name} in {orders_time_policy}")
        yield self.environment.timeout(orders_time_policy)

        print(
            f"The {self.name} has finished preparing the order {order.order_id} for the {order.client.name} in {orders_time_policy}")
        self.environment.ready_orders.put(order)

    def receiving_order_time_policy(self, order):
        return random.randrange(1, 12)

    def accept_order_policy(self, order):
        return self.available
