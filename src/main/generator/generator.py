from abc import abstractmethod, ABC

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv


class Generator(ABC):

    @abstractmethod
    def generate(self, env: FoodDeliverySimpyEnv): pass
