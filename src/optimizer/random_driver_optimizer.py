import random

from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.optimizer.optimizer import Optimizer
from src.order.order import Order


class RandomDriverOptimizer(Optimizer):
    def __init__(self, environment: FoodDeliveryEnvironment):
        super().__init__(environment)

    def select_driver(self, order: Order):
        drivers = self.available_drivers(order)
        return random.choice(drivers)
