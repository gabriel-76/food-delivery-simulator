from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.generator import Generator
from src.main.optimizer.optimizer import Optimizer
from src.main.statistic.statistic import Statistic


class Simulator:
    def __init__(
            self,
            environment: FoodDeliveryEnvironment,
            generators: [Generator],
            optimizer: Optimizer | None = None,
            statistic: Statistic = None,
            debug: bool = False,
    ):
        self.environment = environment
        self.optimizer = optimizer
        self.generators = generators
        self.debug = debug
        self.statistic = statistic
        self.initialize()

    def step(self):
        self.environment.step()

    def run(self, until):
        self.environment.run(until=until)

        if self.debug:
            self.log_events()

        if self.statistic:
            self.statistic.log()

    def initialize(self):
        for generator in self.generators:
            self.environment.process(generator.generate())

        if self.optimizer:
            self.environment.process(self.optimizer.optimize())

    def log_events(self):
        for event in self.environment.events.items:
            print(event)
