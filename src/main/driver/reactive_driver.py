from src.main.driver.capacity import Capacity
from src.main.driver.driver import Driver, DriverStatus
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.route.route import Route


class ReactiveDriver(Driver):
    def __init__(
            self,
            environment: FoodDeliverySimpyEnv,
            coordinates, capacity: Capacity,
            available: bool,
            status: DriverStatus,
            movement_rate,
            max_distance
    ):
        super().__init__(environment, coordinates, capacity, available, status, movement_rate)
        self.max_distance = max_distance
        self.environment.process(self.search_order())

    def accept_route_condition(self, route: Route):
        default_condition = super().accept_route_condition(route)
        order = route.segments[0].order
        collection_coordinate = self.environment.map.distance(self.coordinates, order.restaurant.coordinates)
        return default_condition and collection_coordinate <= self.max_distance

    def search_order(self):
        while True:
            if self.available and self.status is DriverStatus.AVAILABLE and self.environment.count_ready_orders() > 0:
                search_timeout = self.environment.timeout(20)
                order_request = self.environment.ready_orders.get(self.accept_route_condition)
                search_result = yield self.environment.any_of([order_request, search_timeout])
                if order_request in search_result:
                    # print(self.environment.now, f"Driver {self.driver_id} get order {order_request.value.order_id}")
                    self.accept_route(order_request.value)
                    # yield self.environment.timeout(5)
                # else:
                #     print(self.environment.now, f"Driver {self.driver_id} failure search order")
            yield self.environment.timeout(1)
