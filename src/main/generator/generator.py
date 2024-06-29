from abc import abstractmethod, ABC

from src.main.environment.delivery_environment import DeliveryEnvironment


class Generator(ABC):

    @abstractmethod
    def generate(self, env: DeliveryEnvironment): pass
