import random

from src.main.base.dimensions import Dimensions
from src.main.driver.capacity import Capacity
from src.main.driver.driver import Driver
from src.main.driver.driver_actor import DriverActor, DriverStatus
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_generator import TimeShiftGenerator


class TimeShiftDriverGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift=1):
        super().__init__(function, time_shift)

    def run(self, env: FoodDeliverySimpyEnv):
        capacity = Capacity(Dimensions(10, 10, 10, 10))
        drivers = [
            DriverActor(
                environment=env,
                driver=Driver(
                    coordinate=env.map.random_point(),
                    capacity=capacity,
                    available=True,
                    status=DriverStatus.AVAILABLE,
                    movement_rate=random.uniform(1, 30)
                )
            ) for _ in self.range(env)
        ]
        env.add_drivers(drivers)
