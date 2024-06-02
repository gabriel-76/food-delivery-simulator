import random

from src.main.driver.driver import Driver
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.order.order import Order


class FreightEstimate:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def estimate(self, order: Order, driver: Driver):
        total_distance = self.environment.map.total_distance(order, driver)
        return total_distance * random.randrange(0, 3)
