from abc import abstractmethod, ABC
import random

import numpy as np

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv


class Generator(ABC):

    def __init__(self):
        self.python_random = random.Random()

    @abstractmethod
    def generate(self, env: FoodDeliverySimpyEnv): pass

    def reset(self, seed: int | None = None):
        self.seed(seed)

    def seed(self, seed: int | None = None):
        if seed is not None:
            self.random_generator = np.random.default_rng(seed)
            self.python_random.seed(seed)