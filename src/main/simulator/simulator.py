from src.main.client.client_generator import ClientGenerator
from src.main.driver.driver_generator import DriverGenerator
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.optimizer.optimizer import Optimizer
from src.main.order.order_generator import OrderGenerator
from src.main.restaurant.restaurant_generator import RestaurantGenerator


class Simulator:
    def __init__(
            self,
            environment: FoodDeliveryEnvironment,
            client_generator: ClientGenerator,
            restaurant_generator: RestaurantGenerator,
            driver_generator: DriverGenerator,
            order_generator: OrderGenerator,
            optimizer: Optimizer,
            debug: bool = False,
    ):
        self.environment = environment
        self.optimizer = optimizer
        self.client_generator = client_generator
        self.restaurant_generator = restaurant_generator
        self.driver_generator = driver_generator
        self.order_generator = order_generator
        self.debug = debug

    def run(self, until):
        self.environment.process(self.client_generator.generate())
        self.environment.process(self.restaurant_generator.generate())
        self.environment.process(self.driver_generator.generate())
        self.environment.process(self.order_generator.generate())
        self.environment.process(self.optimizer.optimize())
        self.environment.run(until=until)

        if self.debug:
            self.log_events()

    def log_events(self):
        for event in self.environment.events.items:
            print(event)
