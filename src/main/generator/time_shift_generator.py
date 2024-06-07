from abc import abstractmethod, ABC

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.generator import Generator


class TimeShiftGenerator(Generator, ABC):

    def __init__(self, environment: FoodDeliveryEnvironment, time_shift=1):
        super().__init__(environment)
        self.time_shift = time_shift

    @abstractmethod
    def run(self): pass

    def generate(self):
        while True:
            self.run()
            yield self.environment.timeout(self.time_shift)
