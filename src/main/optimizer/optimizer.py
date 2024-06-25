from abc import ABC, abstractmethod

from src.main.cost.cost_function import CostFunction
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.order import Order
from src.main.route.delivery_route_segment import DeliveryRouteSegment
from src.main.route.pickup_route_segment import PickupRouteSegment
from src.main.route.route import Route


class Optimizer(TimeShiftGenerator, ABC):

    def __init__(self, cost_function: CostFunction | None = None, use_estimate=False, time_shift=1):
        super().__init__(time_shift=time_shift)
        self.use_estimate = use_estimate
        self.cost_function = cost_function

    @abstractmethod
    def select_driver(self, env: FoodDeliverySimpyEnv, route: Route):
        pass

    def process_orders(self, env: FoodDeliverySimpyEnv, orders: [Order], rejected=False):
        for order in orders:
            segment_pickup = PickupRouteSegment(order)
            segment_delivery = DeliveryRouteSegment(order)
            route = Route(env, [segment_pickup, segment_delivery])

            driver = self.select_driver(env, route)

            if driver is not None:
                driver.receive_route_requests(route)
            elif rejected:
                env.add_rejected_delivery(order)
            elif self.use_estimate:
                env.add_estimated_order(order)
            else:
                env.add_ready_order(order)

    def optimize(self, env: FoodDeliverySimpyEnv):
        orders = env.get_rejected_deliveries()
        self.process_orders(env, orders, rejected=True)

        if self.use_estimate:
            orders = env.get_estimated_orders()
            self.process_orders(env, orders)
        else:
            orders = env.get_ready_orders()
            self.process_orders(env, orders)

    def run(self, env: FoodDeliverySimpyEnv):
        self.optimize(env)
