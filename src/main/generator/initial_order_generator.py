import random

from src.main.environment.delivery_environment import DeliveryEnvironment
from src.main.generator.initial_generator import InitialGenerator
from src.main.models.order import Order


class InitialOrderGenerator(InitialGenerator):
    def __init__(self, num_orders):
        self.num_orders = num_orders

    def run(self, env: DeliveryEnvironment):
        for _ in range(self.num_orders):
            establishment = random.choice(env.state.establishments)
            customer = random.choice(env.state.customers)

            items = random.sample(establishment._catalog._items, 2)

            order = Order(customer, establishment, env.now, items)

            env.state.add_orders([order])

            customer.place(order, establishment)
