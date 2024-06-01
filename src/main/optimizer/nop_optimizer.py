from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.optimizer.optimizer import Optimizer


class NopOptimizer(Optimizer):
    def __init__(self, environment: FoodDeliveryEnvironment):
        super().__init__(environment)

    def optimize(self):
        yield self.environment.timeout(1)
