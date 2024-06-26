import random

from src.main.actors.driver_actor import DriverStatus
from src.main.base.dimensions import Dimensions
from src.main.driver.capacity import Capacity
from src.main.driver.driver import Driver
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_generator import InitialGenerator


class InitialDriverGenerator(InitialGenerator):
    def __init__(self, num_drivers):
        self.num_drivers = num_drivers

    def run(self, env: FoodDeliverySimpyEnv):
        capacity = Capacity(Dimensions(100, 100, 100, 100))
        drivers = [
            Driver(
                coordinate=env.map.random_point(),
                capacity=capacity,
                available=True,
                status=DriverStatus.AVAILABLE,
                movement_rate=random.uniform(1, 10)
            )
            for _ in range(self.num_drivers)
        ]
        env.add_drivers(drivers)
