import random

from simpy import Environment

from src import FoodDeliveryEnvironment
from src.order.order import Order
from src.restaurant.restaurant import Restaurant


class Client:
    def __init__(self, environment: FoodDeliveryEnvironment, name, coordinates):
        self.environment = environment
        self.name = name
        self.coordinates = coordinates

    def place_order(self, order: Order, restaurant: Restaurant):
        print(f"Customer {self.name} placed an order_{order.order_id} with restaurant {restaurant.name}")
        restaurant.receive_orders([order])
