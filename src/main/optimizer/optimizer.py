import random

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.order.order import Order


class Optimizer:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def select_driver(self, order: Order):
        drivers = self.available_drivers(order)
        return random.choice(drivers)

    def available_drivers(self, order: Order):
        return [driver for driver in self.environment.drivers if driver.check_availability(order)]

    def optimize(self):
        while True:
            while self.environment.count_rejected_delivery_orders() > 0:
                order = yield self.environment.get_rejected_delivery_order()
                driver = self.select_driver(order)
                self.environment.process(driver.deliver_order(order))
            while self.environment.count_ready_orders() > 0:
                order = yield self.environment.get_ready_order()
                driver = self.select_driver(order)
                self.environment.process(driver.deliver_order(order))
            yield self.environment.timeout(self.optimize_time_policy())

    def optimize_time_policy(self):
        return 1
