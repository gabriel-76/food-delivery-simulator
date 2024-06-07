from collections import defaultdict

from src.main.generator.client_generator import ClientGenerator
from src.main.generator.driver_generator import DriverGenerator
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.generator import Generator
from src.main.generator.initial_generator import InitialGenerator
from src.main.optimizer.optimizer import Optimizer
from src.main.generator.order_generator import OrderGenerator
from src.main.generator.restaurant_generator import RestaurantGenerator


class Simulator:
    def __init__(
            self,
            environment: FoodDeliveryEnvironment,
            generators: [Generator],
            optimizer: Optimizer | None = None,
            debug: bool = False,
            statistics: bool = False,
    ):
        self.environment = environment
        self.optimizer = optimizer
        self.generators = generators
        self.debug = debug
        self.statistics = statistics

    def run(self, until):
        for generator in self.generators:
            self.environment.process(generator.generate())
        if self.optimizer:
            self.environment.process(self.optimizer.optimize())
        self.environment.run(until=until)

        if self.debug:
            self.log_events()

        if self.statistics:
            print()
            print("TOTAL RESTAURANTS", len(self.environment.restaurants))
            print("TOTAL CLIENTS", len(self.environment.clients))
            print("TOTAL DRIVERS", len(self.environment.drivers))
            print("TOTAL ORDERS", len(self.environment.orders))
            print()

            print("ORDERS")
            order_status_counts = defaultdict(int)
            for order in self.environment.orders:
                order_status_counts[order.status.name] += 1

            for status, count in order_status_counts.items():
                print(f"{status} {count}")

            print()

            print("DRIVERS")
            drivers_status_counts = defaultdict(int)
            for driver in self.environment.drivers:
                drivers_status_counts[driver.status.name] += 1

            for status, count in drivers_status_counts.items():
                print(f"{status} {count}")

            # self.environment.orders.sort(key=lambda x: x.status)
            #
            # for k, g in groupby(self.environment.orders, key=lambda order: order.status):
            #     print(k.name, len(list(g)))

    def log_events(self):
        for event in self.environment.events.items:
            print(event)
