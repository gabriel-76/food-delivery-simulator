from abc import abstractmethod, ABC

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.generator import Generator


class TimeShiftGenerator(Generator, ABC):

    def __init__(self, function, time_shift=1):
        self.function = function
        self.time_shift = time_shift

    @abstractmethod
    def run(self, env: FoodDeliveryEnvironment): pass

    def range(self, env: FoodDeliveryEnvironment):
        return range(round(self.function(env.now)))

    def generate(self, env: FoodDeliveryEnvironment):
        while True:
            self.run(env)
            yield env.timeout(self.time_shift)
