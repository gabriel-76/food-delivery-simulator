import random

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.order import Order


class TimeShiftOrderGenerator(TimeShiftGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, function, time_shift=1):
        super().__init__(environment, function, time_shift)

    def run(self):

        orders = []

        for _ in self.range():
            client = random.choice(self.environment.clients)
            restaurant = random.choice(self.environment.restaurants)
            items = random.sample(restaurant.catalog.items, 2)
            order = Order(client, restaurant, self.environment.now, items)
            orders.append(order)
            client.place_order(order, restaurant)

        self.environment.orders += orders
