import random

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.driver.capacity import Capacity
from src.main.driver.driver import Driver, DriverStatus
from src.main.generator.time_shift_generator import TimeShiftGenerator


class TimeShiftDriverGenerator(TimeShiftGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, num_drivers, time_shift=1):
        super().__init__(environment, time_shift)
        self.num_drivers = num_drivers

    def run(self):
        capacity = Capacity(Dimensions(10, 10, 10, 10))
        drivers = [
            Driver(
                environment=self.environment,
                coordinates=self.environment.map.random_point(),
                capacity=capacity,
                available=True,
                status=DriverStatus.AVAILABLE,
                movement_rate=random.uniform(1, 30),
            ) for _ in range(self.num_drivers)
        ]
        self.environment.add_drivers(drivers)
