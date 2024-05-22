from simpy import Environment

from src.order.order import Order
from src.restaurant.restaurant import Restaurant


class Client:
    def __init__(self, environment: Environment, name, coordinates):
        self.environment = environment
        self.name = name
        self.coordinates = coordinates

    def make_a_request(self, order: Order, restaurant: Restaurant):
        time_to_place_an_order = self.time_to_place_an_order()
        print(f"Customer {self.name} placed an order {order.order_id} with restaurant {restaurant.name}")
        yield self.environment.timeout(time_to_place_an_order)


    def time_to_place_an_order(self):
        return 2
