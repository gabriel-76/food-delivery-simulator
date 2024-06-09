import random

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.order.order import Order
from src.main.trip.route import Route, RouteType
from src.main.trip.trip import Trip


class Optimizer:

    def select_driver(self, env: FoodDeliveryEnvironment, trip: Trip):
        drivers = self.available_drivers(env, trip)
        if len(drivers) > 0:
            return random.choice(drivers)
        else:
            return None

    def available_drivers(self, env: FoodDeliveryEnvironment, trip: Trip):
        return [driver for driver in env.state.drivers if driver.check_availability(trip)]

    def optimize(self, env: FoodDeliveryEnvironment):
        while True:
            while env.count_rejected_deliveries() > 0:
                order = yield env.get_rejected_deliveries()

                route_collect = Route(RouteType.COLLECT, order)
                route_delivery = Route(RouteType.DELIVERY, order)
                trip = Trip(env, [route_collect, route_delivery])

                driver = self.select_driver(env, trip)

                if driver is not None:
                    driver.request_delivery(trip)
                # else:
                #     self.environment.add_rejected_delivery_order(order)

            while env.count_ready_orders() > 0:
                order = yield env.get_ready_order()

                route_collect = Route(RouteType.COLLECT, order)
                route_delivery = Route(RouteType.DELIVERY, order)
                trip = Trip(env, [route_collect, route_delivery])

                driver = self.select_driver(env, trip)

                if driver is not None:
                    driver.request_delivery(trip)
                # else:
                #     self.environment.add_ready_order(order)

            yield env.timeout(self.optimize_time_policy())

    def optimize_time_policy(self):
        return 1
