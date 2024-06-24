from src.main.cost.cost_function import CostFunction
from src.main.optimizer.optimizer import Optimizer
from src.main.route.delivery_route_segment import DeliveryRouteSegment
from src.main.route.pickup_route_segment import PickupRouteSegment
from src.main.route.route import Route


class RlOptimizer(Optimizer):

    def __init__(self, use_estimate=False, time_shift=1):
        super().__init__(use_estimate=use_estimate, time_shift=time_shift)
        self.action = None

    def select_driver(self, env, route):
        pass

    def process_orders(self, env, orders, rejected=False):
        if len(orders) == 0 or self.action is None:
            return

        problem = False
        for driver_index, order_indexes in self.action:
            print(f'Driver index: {driver_index}, Order indexes: {order_indexes}')
            if driver_index >= len(env.state.drivers):
                problem = True
                print(f'Driver index {driver_index} is out of bounds')
                # raise ValueError(f'Driver index {driver_index} is out of bounds')
            else:
                driver = env.state.drivers[driver_index]
                for order_index in order_indexes:
                    print(f'\tOrder index: {order_index}')
                    if order_index >= len(orders):
                        problem = True
                        print(f'Order index {order_index} is out of bounds')
                        # raise ValueError(f'Order index {order_index} is out of bounds')
                    else:
                        order = orders[order_index]
                        pickup_segment = PickupRouteSegment(order)
                        delivery_segment = DeliveryRouteSegment(order)
                        route = Route(env, [pickup_segment, delivery_segment])
                        driver.receive_route_requests(route)

