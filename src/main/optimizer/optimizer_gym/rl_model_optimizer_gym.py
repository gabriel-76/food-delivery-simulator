from typing import List

from stable_baselines3 import PPO

from src.main.driver.driver import Driver
from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv
from src.main.optimizer.optimizer_gym.optmizer_gym import OptimizerGym
from src.main.route.route import Route


class RLModelOptimizerGym(OptimizerGym):

    def __init__(self, environment: FoodDeliveryGymEnv, model: PPO):
        super().__init__(environment)
        self.model = model

    def get_title(self):
        return "Otimizador por Aprendizado por Reforço"

    def select_driver(self, obs: dict, drivers: List[Driver], route: Route):
        action, _states = self.model.predict(obs)
        return action
