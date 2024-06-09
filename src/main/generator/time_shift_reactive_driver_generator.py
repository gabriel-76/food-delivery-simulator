import random

from src.main.base.dimensions import Dimensions
from src.main.generator.time_shift_driver_generator import TimeShiftDriverGenerator
from src.main.driver.reactive_driver import ReactiveDriver
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.driver.capacity import Capacity
from src.main.driver.driver import DriverStatus


class TimeShiftReactiveDriverGenerator(TimeShiftDriverGenerator):
    def __init__(self, function, time_shift=1):
        super().__init__(function, time_shift)

    def run(self, env: FoodDeliveryEnvironment):
        capacity = Capacity(Dimensions(10, 10, 10, 10))
        drivers = [
            ReactiveDriver(
                environment=env,
                coordinates=env.map.random_point(),
                capacity=capacity,
                available=True,
                status=DriverStatus.AVAILABLE,
                movement_rate=random.uniform(1, 30),
                max_distance=random.randrange(100, 300)
            ) for _ in self.range(env)
        ]
        env.add_drivers(drivers)
