import random

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.order import Order
from src.main.trip.route import Route, RouteType
from src.main.trip.trip import Trip


class Optimizer(TimeShiftGenerator):

    def __init__(self, time_shift=1):
        super().__init__(time_shift=time_shift)

    def select_driver(self, env: FoodDeliveryEnvironment, trip: Trip):
        drivers = self.available_drivers(env, trip)
        if len(drivers) > 0:
            return random.choice(drivers)
        else:
            return None

    def available_drivers(self, env: FoodDeliveryEnvironment, trip: Trip):
        return [driver for driver in env.state.drivers if driver.check_availability(trip)]

    def process_orders(self, env: FoodDeliveryEnvironment, orders: [Order]):
        for order in orders:
            route_collect = Route(RouteType.COLLECT, order)
            route_delivery = Route(RouteType.DELIVERY, order)
            trip = Trip(env, [route_collect, route_delivery])

            driver = self.select_driver(env, trip)

            if driver is not None:
                driver.request_delivery(trip)
            else:
                env.add_rejected_delivery(order)

    def optimize(self, env: FoodDeliveryEnvironment):
        orders = yield env.process(env.get_rejected_deliveries())
        self.process_orders(env, orders)

        orders = yield env.process(env.get_ready_orders())
        self.process_orders(env, orders)

    def run(self, env: FoodDeliveryEnvironment):
        env.process(self.optimize(env))
