import random

from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.driver.driver import DriverStatus


class Optimizer:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def optimize(self):
        while True:
            drivers = [driver for driver in self.environment.drivers if
                       driver.available and driver.status is DriverStatus.WAITING]
            while self.environment.count_rejected_delivery_orders() > 0:
                order = yield self.environment.get_rejected_delivery_order()
                filtered_drivers = [d for d in drivers if d.fits(order)]
                driver = random.choice(filtered_drivers)
                self.environment.process(driver.deliver_order(order))
            while self.environment.count_ready_orders() > 0:
                order = yield self.environment.get_ready_order()
                filtered_drivers = [d for d in drivers if d.fits(order)]
                driver = random.choice(filtered_drivers)
                self.environment.process(driver.deliver_order(order))
            yield self.environment.timeout(self.optimize_time_policy())

    def optimize_time_policy(self):
        return 1
