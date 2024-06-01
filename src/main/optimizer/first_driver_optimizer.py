from src.main.environment import FoodDeliveryEnvironment
from src.main.optimizer.optimizer import Optimizer
from src.main.order.order import Order


class FirstDriverOptimizer(Optimizer):
    def __init__(self, environment: FoodDeliveryEnvironment):
        super().__init__(environment)

    def select_driver(self, order: Order):
        drivers = self.available_drivers(order)
        return drivers[0]
