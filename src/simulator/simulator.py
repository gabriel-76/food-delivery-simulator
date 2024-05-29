from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.client.client_generator import ClientGenerator
from src.driver.driver_generator import DriverGenerator
from src.optimizer.optimizer import Optimizer
from src.order.order_generator import OrderGenerator
from src.restaurant.restaurant_generator import RestaurantGenerator


class Simulator:
    def __init__(
            self,
            environment: FoodDeliveryEnvironment,
            client_generator: ClientGenerator,
            restaurant_generator: RestaurantGenerator,
            driver_generator: DriverGenerator,
            order_generator: OrderGenerator,
            optimizer: Optimizer,
    ):
        self.environment = environment
        self.optimizer = optimizer
        self.client_generator = client_generator
        self.restaurant_generator = restaurant_generator
        self.driver_generator = driver_generator
        self.order_generator = order_generator

    def run(self, until):
        self.environment.process(self.client_generator.generate())
        self.environment.process(self.restaurant_generator.generate())
        self.environment.process(self.driver_generator.generate())
        self.environment.process(self.order_generator.generate())
        self.environment.process(self.optimizer.optimize())
        self.environment.run(until=until)
