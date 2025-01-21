from abc import abstractmethod, ABC

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.generator import Generator


class InitialGenerator(Generator, ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def run(self, env: FoodDeliverySimpyEnv): pass

    def generate(self, env: FoodDeliverySimpyEnv):
        self.run(env)
        yield env.timeout(0)
