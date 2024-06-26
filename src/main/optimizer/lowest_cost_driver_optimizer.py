from src.main.actors import DriverActor
from src.main.cost.cost_function import CostFunction
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.optimizer.optimizer import Optimizer
from src.main.route.route import Route


class LowestCostDriverOptimizer(Optimizer):
    def __init__(self, cost_function: CostFunction, time_shift=1):
        super().__init__(cost_function, time_shift)

    def compare_distance(self, env: FoodDeliverySimpyEnv, driver: DriverActor, route: Route):
        return self.cost_function.cost(env.map, driver, route.route_segments[0])

    def select_driver(self, env: FoodDeliverySimpyEnv, route: Route):
        drivers = env.available_drivers(route)
        # drivers = list(filter(lambda driver: driver.current_route is None or
        # driver.current_route.size() <= 1, drivers))
        nearest_driver = min(drivers, key=lambda driver: self.compare_distance(env, driver, route))
        return nearest_driver
