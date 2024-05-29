from src import FoodDeliveryEnvironment
from src.client.client_factory import ClientFactory
from src.driver.driver_factory import DriverFactory
from src.optimizer.optimizer import Optimizer
from src.order.order_factory import OrderFactory
from src.restaurant.restaurant_factory import RestaurantFactory

NUM_DRIVERS = 50
SIMULATION_TIME = 1000000


class Simulator:
    def __init__(
            self,
            environment: FoodDeliveryEnvironment,
            optimizer: Optimizer,
            client_factory: ClientFactory,
            restaurant_factory: RestaurantFactory,
            driver_factory: DriverFactory,
            order_factory: OrderFactory,
    ):
        self.environment = environment
        self.optimizer = optimizer
        self.client_factory = client_factory
        self.restaurant_factory = restaurant_factory
        self.driver_factory = driver_factory
        self.order_factory = order_factory

    def run(self):
        clients = self.client_factory.clients_generation_policy()
        restaurants = self.restaurant_factory.restaurants_generation_policy()
        drivers = self.driver_factory.drivers_generation_policy()

        self.environment.process(self.order_factory.order_generation_policy(clients, restaurants))

        self.environment.process(self.optimizer.optimize(drivers))
