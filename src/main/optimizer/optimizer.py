import random

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.order.order import Order
from src.main.trip.route import Route, RouteType
from src.main.trip.trip import Trip


class Optimizer:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def select_driver(self, trip: Trip):
        drivers = self.available_drivers(trip)
        return random.choice(drivers)

    def available_drivers(self, trip: Trip):
        return [driver for driver in self.environment.drivers if driver.check_availability(trip)]

    def optimize(self):
        while True:
            # print("Optimizing...")
            while self.environment.count_rejected_delivery_orders() > 0:
                order = yield self.environment.get_rejected_delivery_order()
                driver = self.select_driver(order)
                self.environment.process(driver.deliver_order(order))
            while self.environment.count_ready_orders() > 0:
                print(self.environment.count_ready_orders())
                order = yield self.environment.get_ready_order()

                route_collect = Route(RouteType.COLLECT, order)
                route_delivery = Route(RouteType.DELIVERY, order)
                trip = Trip(self.environment, [route_collect, route_delivery])

                driver = self.select_driver(trip)
                print(driver)
                self.environment.process(driver.deliver_order(trip))
            yield self.environment.timeout(self.optimize_time_policy())

    def optimize_time_policy(self):
        return 1
