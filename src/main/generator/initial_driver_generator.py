import random

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_generator import InitialGenerator
from src.main.models.commons.capacity import Capacity
from src.main.models.commons.dimension import Dimension
from src.main.models.driver.driver import Driver


class InitialDriverGenerator(InitialGenerator):
    def __init__(self, num_drivers):
        self.num_drivers = num_drivers

    def run(self, env: FoodDeliverySimpyEnv):
        capacity = Capacity(Dimension(100, 100, 100, 100))
        drivers = [
            Driver(
                coordinate=env.map.random_point(),
                capacity=capacity,
                movement_rate=random.uniform(1, 10)
            )
            for _ in range(self.num_drivers)
        ]
        env.add_drivers(drivers)
