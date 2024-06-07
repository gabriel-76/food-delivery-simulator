import random

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.order import Order


class OrderGenerator(TimeShiftGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, num_orders):
        super().__init__(environment)
        self.num_orders = num_orders

    def run(self):
        clients = self.environment.clients
        restaurants = self.environment.restaurants
        selected_clients = random.sample(clients, 1)
        selected_restaurants = random.sample(restaurants, 1)

        for client in selected_clients:
            restaurant = random.choice(selected_restaurants)

            items = random.sample(restaurant.catalog.items, 2)

            x = self.environment.now

            orders = [Order(client, restaurant, self.environment.now, items) for _ in range(self.num_orders)]

            for order in orders:
                client.place_order(order, restaurant)

            self.environment.orders += orders
