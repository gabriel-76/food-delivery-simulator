import random

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.order import Order


class TimeShiftOrderGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift=1):
        super().__init__(function, time_shift)

    def run(self, env: FoodDeliverySimpyEnv):

        orders = []

        for _ in self.range(env):
            customer = random.choice(env.state.customers)
            establishment = random.choice(env.state.establishments)
            items = random.sample(establishment.catalog.items, 2)
            order = Order(customer, establishment, env.now, items)
            orders.append(order)
            customer.place_order(order, establishment)

        env.state.orders += orders
