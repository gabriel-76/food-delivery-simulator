import random

from src.main.base.dimensions import Dimensions
from src.main.driver.capacity import Capacity
from src.main.driver.driver import Driver, DriverStatus
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_generator import InitialGenerator


class InitialDriverGenerator(InitialGenerator):
    def __init__(self, num_drivers, desconsider_capacity=False):
        self.num_drivers = num_drivers
        self.desconsider_capacity = desconsider_capacity

    def run(self, env: FoodDeliverySimpyEnv):
        capacity = Capacity(Dimensions(100, 100, 100, 100))
        if self.desconsider_capacity:
            capacity = Capacity(Dimensions(float('inf'), float('inf'), float('inf'), float('inf')))

        drivers = [
            Driver(
                environment=env,
                coordinate=env.map.random_point(),
                capacity=capacity,
                available=True,
                status=DriverStatus.AVAILABLE,
                movement_rate=random.uniform(1, 10),
            ) for _ in range(self.num_drivers)
        ]
        env.add_drivers(drivers)
