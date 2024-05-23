import random

from simpy import Environment

from src.restaurant.catalog import Catalog


class Restaurant:
    def __init__(
            self,
            environment: Environment,
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

    def receiving_orders(self, order):
        orders_time_policy = self.receiving_orders_time_policy(order)
        print(f"The {self.name} is preparing the order {order.order_id} for the {order.client.name} in {orders_time_policy}")
        yield self.environment.timeout(orders_time_policy)


    def receiving_orders_time_policy(self, order):
        return random.randrange(1, 12)

