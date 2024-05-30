import random

from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.base.dimensions import Dimensions
from src.driver.capacity import Capacity
from src.driver.driver import Driver, DriverStatus

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
                    status=DriverStatus.WAITING
                ) for _ in range(random.randrange(0, NUM_DRIVERS))
            ]
            self.environment.add_drivers(drivers)
            yield self.environment.timeout(1)
