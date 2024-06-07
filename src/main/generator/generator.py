from abc import abstractmethod, ABC

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment


class Generator(ABC):

    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    @abstractmethod
    def generate(self): pass
