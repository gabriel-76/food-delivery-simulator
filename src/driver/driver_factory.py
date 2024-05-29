from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.base.dimensions import Dimensions
from src.driver.capacity import Capacity
from src.driver.driver import Driver

NUM_DRIVERS = 50


class DriverFactory:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def drivers_generation_policy(self):
        capacity = Capacity(Dimensions(10, 10, 10, 10))
        return [Driver(self.environment, f"driver_{i}", (), f"type_{i}", capacity, True) for i in range(NUM_DRIVERS)]
