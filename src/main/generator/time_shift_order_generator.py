import random

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.order import Order


class TimeShiftOrderGenerator(TimeShiftGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, function, time_shift=1):
        super().__init__(environment, function, time_shift)

    def run(self):
        clients = self.environment.clients
        restaurants = self.environment.restaurants
        selected_clients = random.sample(clients, 1)
        selected_restaurants = random.sample(restaurants, 1)

        for client in selected_clients:
            restaurant = random.choice(selected_restaurants)

            items = random.sample(restaurant.catalog.items, 2)

            x = self.environment.now

            orders = [
                Order(client, restaurant, self.environment.now, items)
                for _ in self.range()
            ]

            for order in orders:
                client.place_order(order, restaurant)

            self.environment.orders += orders
