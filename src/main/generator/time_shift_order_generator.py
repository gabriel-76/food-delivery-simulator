import random

from src.main.environment.delivery_environment import DeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.models.order import Order


class TimeShiftOrderGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift=1):
        super().__init__(function, time_shift)

    def run(self, env: DeliveryEnvironment):

        orders = []

        for _ in self.range(env):
            customer = random.choice(env.state.customers)
            establishment = random.choice(env.state.establishments)
            items = random.sample(establishment._catalog._items, 2)
            order = Order(customer, establishment, env.now, items)
            orders.append(order)
            customer.place(order, establishment)

        env.state.add_orders(orders)
