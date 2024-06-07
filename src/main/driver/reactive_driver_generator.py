import random

from src.main.base.dimensions import Dimensions
from src.main.driver.driver_generator import DriverGenerator
from src.main.driver.reactive_driver import ReactiveDriver
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.driver.capacity import Capacity
from src.main.driver.driver import Driver, DriverStatus


class ReactiveDriverGenerator(DriverGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, num_drivers):
        super().__init__(environment)
        self.num_drivers = num_drivers

    def generate(self):
        # while True:
        capacity = Capacity(Dimensions(10, 10, 10, 10))
        drivers = [
            ReactiveDriver(
                environment=self.environment,
                coordinates=self.environment.map.random_point(),
                capacity=capacity,
                available=True,
                status=DriverStatus.AVAILABLE,
                movement_rate=random.uniform(1, 30),
                max_distance=random.randrange(100, 300)
            ) for _ in range(self.num_drivers)
        ]
        self.environment.add_drivers(drivers)
        yield self.environment.timeout(1)
