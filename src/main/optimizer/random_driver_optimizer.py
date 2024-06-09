import random

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.optimizer.optimizer import Optimizer
from src.main.trip.trip import Trip


class RandomDriverOptimizer(Optimizer):

    def select_driver(self, env: FoodDeliveryEnvironment, trip: Trip):
        drivers = env.available_drivers(trip)
        return random.choice(drivers) if len(drivers) > 0 else None
