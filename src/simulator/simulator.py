from src import FoodDeliveryEnvironment
from src.client.client_generator import ClientGenerator
from src.driver.driver_generator import DriverGenerator
from src.optimizer.optimizer import Optimizer
from src.order.order_generator import OrderGenerator
from src.restaurant.restaurant_generator import RestaurantGenerator

NUM_DRIVERS = 50
SIMULATION_TIME = 1000000


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

    def run(self):
        clients = self.client_generator.clients_generation_policy()
        restaurants = self.restaurant_generator.restaurants_generation_policy()
        drivers = self.driver_generator.drivers_generation_policy()

        self.environment.process(self.order_generator.order_generation_policy(clients, restaurants))

        self.environment.process(self.optimizer.optimize(drivers))
