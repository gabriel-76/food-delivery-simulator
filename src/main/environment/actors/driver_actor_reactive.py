from src.main.environment.actors.driver_actor import DriverActor, DriverStatus
from src.main.models.driver import Driver
from src.main.models.route.route import Route
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv


class DriverActorReactive(DriverActor):
    def __init__(
            self,
            environment: FoodDeliverySimpyEnv,
            driver: Driver,
            max_distance: int
    ):
        super().__init__(environment, driver)
        self.max_distance = max_distance
        self.process(self.search_order())

    def accept_route_condition(self, route: Route):
        default_condition = super().accept_route_condition(route)
        order = route._segments[0]._order
        pickup_coordinate = self.environment.map.distance(self.coordinate, order._establishment.coordinate)
        return default_condition and pickup_coordinate <= self.max_distance

    def search_order(self):
        while True:
            if self.available and self.status is DriverStatus.AVAILABLE and self.environment.count_ready_orders() > 0:
                search_timeout = self.timeout(20)
                order_request = self.environment.ready_orders.get(self.accept_route_condition)
                search_result = yield self.environment.any_of([order_request, search_timeout])
                if order_request in search_result:
                    # print(self.now, f"Driver {self.driver_id} get order {order_request.value.order_id}")
                    self.accept_route(order_request.value)
                    # yield self.timeout(5)
                # else:
                #     print(self.now, f"Driver {self.driver_id} failure search order")
            yield self.timeout(1)
