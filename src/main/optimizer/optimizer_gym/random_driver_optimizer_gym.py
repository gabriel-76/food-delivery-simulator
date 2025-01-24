from typing import List

from src.main.driver.driver import Driver
from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv
from src.main.optimizer.optimizer_gym.optmizer_gym import OptimizerGym
from src.main.route.route import Route
from src.main.utils.random_manager import RandomManager


class RandomDriverOptimizerGym(OptimizerGym):
    
    def __init__(self, environment: FoodDeliveryGymEnv, seed: int | None = None):
        super().__init__(environment, seed)
        self.rng = RandomManager().get_random_instance()

    def select_driver(self, drivers: List[Driver], route: Route):
        # drivers = list(filter(lambda driver: driver.current_route is None or
        # driver.current_route.size() <= 1, drivers))
        len_drivers = len(drivers)
        return self.rng.choice(range(len_drivers)) if len_drivers > 0 else None
