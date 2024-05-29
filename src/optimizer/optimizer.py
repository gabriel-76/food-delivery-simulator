import random

from src import FoodDeliveryEnvironment
from src.driver.driver import Driver


class Optimizer:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def optimize(self):
        while True:
            drivers = self.environment.drivers
            while self.environment.count_ready_orders() > 0:
                order = yield self.environment.get_ready_order()
                filtered_drivers = [d for d in drivers if d.fits(order)]
                driver = random.choice(filtered_drivers)
                self.environment.process(driver.deliver_order(order))
            yield self.environment.timeout(1)
