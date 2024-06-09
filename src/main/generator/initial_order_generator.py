import random
from datetime import datetime

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.initial_generator import InitialGenerator
from src.main.order.order import Order


class InitialOrderGenerator(InitialGenerator):
    def __init__(self, num_orders):
        self.num_orders = num_orders

    def run(self, env: FoodDeliveryEnvironment):
        for _ in range(self.num_orders):
            restaurant = random.choice(env.restaurants)
            client = random.choice(env.clients)

            items = random.sample(restaurant.catalog.items, 2)

            order = Order(client, restaurant, env.now, items)

            env.orders += [order]

            client.place_order(order, restaurant)
