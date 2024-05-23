import random

from simpy import Environment

from src.order.order import Order
from src.restaurant.restaurant import Restaurant


class Client:
    def __init__(self, environment: Environment, name, coordinates):
        self.environment = environment
        self.name = name
        self.coordinates = coordinates

    def place_an_order(self, order: Order, restaurant: Restaurant):
        place_an_order_time_policy = self.place_an_order_time_policy()
        print(f"Customer {self.name} placed an order {order.order_id} with restaurant {restaurant.name}")
        yield self.environment.timeout(place_an_order_time_policy)


    def place_an_order_time_policy(self):
        return 1
