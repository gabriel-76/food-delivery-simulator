import random

from src.main.environment.actors import DriverStatus
from src.main.models.base import Dimensions
from src.main.models.driver import Capacity
from src.main.models.driver import Driver
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_driver_generator import TimeShiftDriverGenerator


class TimeShiftReactiveDriverGenerator(TimeShiftDriverGenerator):
    def __init__(self, function, time_shift=1):
        super().__init__(function, time_shift)

    def run(self, env: FoodDeliverySimpyEnv):
        capacity = Capacity(Dimensions(10, 10, 10, 10))
        drivers = [
            Driver(
                coordinate=env.map.random_point(),
                capacity=capacity,
                available=True,
                status=DriverStatus.AVAILABLE,
                movement_rate=random.uniform(1, 30),
                max_distance=random.randrange(100, 300)
            )
            for _ in self.range(env)
        ]
        env.add_drivers(drivers)
