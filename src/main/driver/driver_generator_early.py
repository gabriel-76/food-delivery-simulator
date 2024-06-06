import random

from src.main.base.dimensions import Dimensions
from src.main.driver.driver_generator import DriverGenerator
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.driver.capacity import Capacity
from src.main.driver.driver import Driver, DriverStatus


class DriverGeneratorEarly(DriverGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, num_drivers):
        super().__init__(environment)
        self.environment = environment
        self.num_drivers = num_drivers

    def generate(self):
        capacity = Capacity(Dimensions(100, 100, 100, 100))
        drivers = [
            Driver(
                environment=self.environment,
                coordinates=self.environment.map.random_point(),
                capacity=capacity,
                available=True,
                status=DriverStatus.WAITING,
                movement_rate=random.uniform(1, 30),
            ) for _ in range(self.num_drivers)
        ]
        self.environment.add_drivers(drivers)
        yield self.environment.timeout(1)
