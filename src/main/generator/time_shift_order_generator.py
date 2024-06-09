import random

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.order import Order


class TimeShiftOrderGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift=1):
        super().__init__(function, time_shift)

    def run(self, env: FoodDeliveryEnvironment):

        orders = []

        for _ in self.range(env):
            client = random.choice(env.clients)
            restaurant = random.choice(env.restaurants)
            items = random.sample(restaurant.catalog.items, 2)
            order = Order(client, restaurant, env.now, items)
            orders.append(order)
            client.place_order(order, restaurant)

        env.orders += orders
