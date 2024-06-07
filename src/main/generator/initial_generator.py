from abc import abstractmethod, ABC

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.generator import Generator


class InitialGenerator(Generator, ABC):

    def __init__(self, environment: FoodDeliveryEnvironment):
        super().__init__(environment)

    @abstractmethod
    def run(self): pass

    def generate(self):
        self.run()
        yield self.environment.timeout(0)
