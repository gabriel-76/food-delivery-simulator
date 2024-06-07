from collections import defaultdict

from src.main.generator.time_shift_client_generator import TimeShiftClientGenerator
from src.main.generator.time_shift_driver_generator import TimeShiftDriverGenerator
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.generator import Generator
from src.main.generator.initial_generator import InitialGenerator
from src.main.optimizer.optimizer import Optimizer
from src.main.generator.time_shift_order_generator import TimeShiftOrderGenerator
from src.main.generator.restaurant_generator import RestaurantGenerator
from src.main.statistic.statistic import Statistic


class Simulator:
    def __init__(
            self,
            environment: FoodDeliveryEnvironment,
            generators: [Generator],
            optimizer: Optimizer | None = None,
            debug: bool = False,
            statistic: Statistic = None,
    ):
        self.environment = environment
        self.optimizer = optimizer
        self.generators = generators
        self.debug = debug
        self.statistic = statistic

    def run(self, until):

        for generator in self.generators:
            self.environment.process(generator.generate())

        if self.optimizer:
            self.environment.process(self.optimizer.optimize())

        self.environment.run(until=until)

        if self.debug:
            self.log_events()

        if self.statistic:
            self.statistic.log()

    def log_events(self):
        for event in self.environment.events.items:
            print(event)
