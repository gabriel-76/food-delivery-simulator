from typing import List

from src.main.cost.cost_function import CostFunction
from src.main.driver.driver import Driver
from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv
from src.main.optimizer.optimizer_gym.optmizer_gym import OptimizerGym
from src.main.route.route import Route


class LowestCostDriverOptimizerGym(OptimizerGym):
    
    def __init__(self, environment: FoodDeliveryGymEnv, cost_function: CostFunction | None = None):
        super().__init__(environment)
        self.cost_function = cost_function

    def compare_distance(self, driver: Driver, route: Route):
        map = self.gym_env.simpy_env.map
        return self.cost_function.cost(map, driver, route.route_segments[0])

    def select_driver(self, drivers: List[Driver], route: Route):
        # drivers = list(filter(lambda driver: driver.current_route is None or
        # driver.current_route.size() <= 1, drivers))
        nearest_driver = min(drivers, key=lambda driver: self.compare_distance(driver, route))
        return drivers.index(nearest_driver)
