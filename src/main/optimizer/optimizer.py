from abc import ABC, abstractmethod

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.order import Order
from src.main.trip.route import Route, RouteType
from src.main.trip.trip import Trip


class Optimizer(TimeShiftGenerator, ABC):

    def __init__(self, use_estimate=False, time_shift=1):
        super().__init__(time_shift=time_shift)
        self.use_estimate = use_estimate

    @abstractmethod
    def select_driver(self, env: FoodDeliveryEnvironment, trip: Trip):
        pass

    def process_orders(self, env: FoodDeliveryEnvironment, orders: [Order], rejected=False):
        for order in orders:
            route_collect = Route(RouteType.COLLECT, order)
            route_delivery = Route(RouteType.DELIVERY, order)
            trip = Trip(env, [route_collect, route_delivery])

            driver = self.select_driver(env, trip)

            if driver is not None:
                driver.request_delivery(trip)
            elif rejected:
                env.add_rejected_delivery(order)
            elif self.use_estimate:
                env.add_estimated_order(order)
            else:
                env.add_ready_order(order)

    def optimize(self, env: FoodDeliveryEnvironment):
        orders = yield env.process(env.get_rejected_deliveries())
        self.process_orders(env, orders, rejected=True)

        if self.use_estimate:
            orders = yield env.process(env.get_estimated_orders())
            self.process_orders(env, orders)
        else:
            orders = yield env.process(env.get_ready_orders())
            self.process_orders(env, orders)

    def run(self, env: FoodDeliveryEnvironment):
        env.process(self.optimize(env))
