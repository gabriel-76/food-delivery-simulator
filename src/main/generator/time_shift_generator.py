from abc import abstractmethod, ABC

from src.main.environment.delivery_environment import DeliveryEnvironment
from src.main.generator.generator import Generator


class TimeShiftGenerator(Generator, ABC):

    def __init__(self, function=lambda time: 1, time_shift=1):
        self.function = function
        self.time_shift = time_shift

    @abstractmethod
    def run(self, env: DeliveryEnvironment): pass

    def range(self, env: DeliveryEnvironment):
        return range(round(self.function(env.now)))

    def generate(self, env: DeliveryEnvironment):
        while True:
            self.run(env)
            yield env.timeout(self.time_shift)
