import random

from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.base.dimensions import Dimensions
from src.driver.capacity import Capacity
from src.driver.driver import Driver

NUM_DRIVERS = 50


class DriverGenerator:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def generate(self):
        driver_id = 0
        while True:
            capacity = Capacity(Dimensions(10, 10, 10, 10))
            drivers = [Driver(self.environment, f"driver_{driver_id}", (), f"type_{driver_id}", capacity, True) for i in range(random.randrange(0, NUM_DRIVERS))]
            self.environment.add_drivers(drivers)
            driver_id += 1
            yield self.environment.timeout(1)
