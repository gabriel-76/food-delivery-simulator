import random

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.driver.capacity import Capacity
from src.main.driver.driver import Driver, DriverStatus

NUM_DRIVERS = 50


class DriverGenerator:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def generate(self):
        while True:
            capacity = Capacity(Dimensions(10, 10, 10, 10))
            drivers = [
                Driver(
                    environment=self.environment,
                    coordinates=self.environment.map.random_point(),
                    capacity=capacity,
                    available=True,
                    status=DriverStatus.AVAILABLE,
                    movement_rate=random.uniform(1, 30),
                ) for _ in range(random.randrange(0, NUM_DRIVERS))
            ]
            self.environment.add_drivers(drivers)
            yield self.environment.timeout(1)
