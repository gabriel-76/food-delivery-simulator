import random

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_generator import InitialGenerator
from src.main.order.order import Order


class InitialOrderGenerator(InitialGenerator):
    def __init__(self, num_orders):
        self.num_orders = num_orders

    def run(self, env: FoodDeliverySimpyEnv):
        for _ in range(self.num_orders):
            restaurant = random.choice(env.state.restaurants)
            customer = random.choice(env.state.customers)

            items = random.sample(restaurant.catalog.items, 2)

            order = Order(customer, restaurant, env.now, items)

            env.state.orders += [order]

            customer.place_order(order, restaurant)
