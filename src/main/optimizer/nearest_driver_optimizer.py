from src.main.driver.driver_actor import DriverActor
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.optimizer.optimizer import Optimizer
from src.main.route.route import Route


class NearestDriverOptimizer(Optimizer):
    def __init__(self, time_shift=1):
        super().__init__(time_shift=time_shift)

    def compare_distance(self, env: FoodDeliverySimpyEnv, driver: DriverActor, route: Route):
        return env.map.distance(driver.coordinate, route.route_segments[0].coordinate)

    def select_driver(self, env: FoodDeliverySimpyEnv, route: Route):
        drivers = env.available_drivers(route)
        # drivers = list(filter(lambda driver: driver.current_route is None or
        # driver.current_route.size() <= 1, drivers))
        nearest_driver = min(drivers, key=lambda driver: self.compare_distance(env, driver, route))
        return nearest_driver
