from abc import ABC, abstractmethod

from src.main.environment.delivery_environment import DeliveryEnvironment


class Metric(ABC):

    def __init__(self, environment: DeliveryEnvironment):
        self.environment = environment

    @abstractmethod
    def view(self, ax) -> None:
        pass
