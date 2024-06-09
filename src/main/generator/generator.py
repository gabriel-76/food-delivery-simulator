from abc import abstractmethod, ABC

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment


class Generator(ABC):

    @abstractmethod
    def generate(self, env: FoodDeliveryEnvironment): pass
