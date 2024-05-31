from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.optimizer.optimizer import Optimizer
from src.order.order import Order


class FirstDriverOptimizer(Optimizer):
    def __init__(self, environment: FoodDeliveryEnvironment):
        super().__init__(environment)

    def select_driver(self, order: Order):
        drivers = self.available_drivers(order)
        return drivers[0]
