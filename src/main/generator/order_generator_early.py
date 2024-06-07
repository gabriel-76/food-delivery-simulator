import random
from datetime import datetime

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.order.order import Order
from src.main.generator.order_generator import OrderGenerator


class OrderGeneratorEarly(OrderGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, num_orders):
        super().__init__(environment)
        self.environment = environment
        self.num_orders = num_orders

    def generate(self):
        for _ in range(self.num_orders):
            restaurant = random.choice(self.environment.restaurants)
            client = random.choice(self.environment.clients)

            items = random.sample(restaurant.catalog.items, 2)

            order = Order(client, restaurant, datetime.now(), items)

            self.environment.orders += [order]

            client.place_order(order, restaurant)

        yield self.environment.timeout(1)
