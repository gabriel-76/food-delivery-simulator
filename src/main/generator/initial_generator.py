from abc import abstractmethod, ABC

from src.main.environment.delivery_environment import DeliveryEnvironment
from src.main.generator.generator import Generator


class InitialGenerator(Generator, ABC):

    @abstractmethod
    def run(self, env: DeliveryEnvironment): pass

    def generate(self, env: DeliveryEnvironment):
        self.run(env)
        yield env.timeout(0)
