from typing import List

from src.main.driver.driver import Driver
from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv
from src.main.optimizer.optimizer_gym.optmizer_gym import OptimizerGym
from src.main.route.route import Route
from src.main.utils.random_manager import RandomManager


class RandomDriverOptimizerGym(OptimizerGym):

    def select_driver(self, drivers: List[Driver], route: Route):
        return self.gym_env.action_space.sample()
