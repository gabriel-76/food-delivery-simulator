import random
from datetime import datetime

from src import FoodDeliveryEnvironment
from src.client.client import Client
from src.order.order import Order
from src.restaurant.restaurant import Restaurant


class OrderFactory:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def order_generation_policy(self, clients: [Client], restaurants: [Restaurant]):
        order_id = 0
        while True:
            selected_clients = random.sample(clients, 1)
            selected_restaurants = random.sample(restaurants, 1)

            for client in selected_clients:
                restaurant = random.choice(selected_restaurants)

                items = random.sample(restaurant.catalog.items, 2)

                order = Order(str(order_id), client, restaurant, datetime.now(), items)

                client.place_order(order, restaurant)

                order_id += 1
            yield self.environment.timeout(random.expovariate(1.0 / 2))