from abc import ABC, abstractmethod

from src.main.cost.cost_function import CostFunction
from src.main.environment.delivery_environment import DeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.models.order.order import Order
from src.main.models.order.rejection import SystemRejection
from src.main.models.route.route import Route
from src.main.models.route.segment import PickupSegment, DeliverySegment


class Optimizer(TimeShiftGenerator, ABC):

    def __init__(self, cost_function: CostFunction | None = None, time_shift=1):
        super().__init__(time_shift=time_shift)
        self.cost_function = cost_function

    @abstractmethod
    def select_driver(self, env: DeliveryEnvironment, route: Route):
        pass

    def process_orders(self, env: DeliveryEnvironment, orders: [Order]):
        for order in orders:
            segment_pickup = PickupSegment(order)
            segment_delivery = DeliverySegment(order)
            route = Route([segment_pickup, segment_delivery])

            driver = self.select_driver(env, route)

            if driver is not None:
                env.deliver(route, driver)
            else:
                env.add_rejected_delivery(order, SystemRejection(env.now))

    def optimize(self, env: DeliveryEnvironment):
        orders = env.get_ready_orders()
        self.process_orders(env, orders)

    def run(self, env: DeliveryEnvironment):
        self.optimize(env)
