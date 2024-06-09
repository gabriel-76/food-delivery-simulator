from abc import abstractmethod, ABC

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.generator import Generator


class InitialGenerator(Generator, ABC):

    @abstractmethod
    def run(self, env: FoodDeliveryEnvironment): pass

    def generate(self, env: FoodDeliveryEnvironment):
        self.run(env)
        yield env.timeout(0)
