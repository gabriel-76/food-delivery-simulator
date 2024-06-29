import random

from src.main.environment.delivery_environment import DeliveryEnvironment
from src.main.optimizer.optimizer import Optimizer
from src.main.models.route.route import Route


class RandomDriverOptimizer(Optimizer):
    def __init__(self, time_shift=1):
        super().__init__(time_shift=time_shift)

    def select_driver(self, env: DeliveryEnvironment, route: Route):
        drivers = env.available_drivers(route)
        return random.choice(drivers) if len(drivers) > 0 else None
