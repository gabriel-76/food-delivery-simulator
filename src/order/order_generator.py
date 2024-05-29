import random
from datetime import datetime

from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.order.order import Order


class OrderGenerator:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def generate(self):
        while True:
            clients = self.environment.clients
            restaurants = self.environment.restaurants
            selected_clients = random.sample(clients, 1)
            selected_restaurants = random.sample(restaurants, 1)

            for client in selected_clients:
                restaurant = random.choice(selected_restaurants)

                items = random.sample(restaurant.catalog.items, 2)

                order = Order(client, restaurant, datetime.now(), items)

                client.place_order(order, restaurant)

            yield self.environment.timeout(1)
