from src.main.client.client import Client
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.initial_generator import InitialGenerator


class ClientGeneratorEarly(InitialGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, num_clients):
        super().__init__(environment)
        self.num_clients = num_clients

    def run(self):
        clients = [
            Client(
                environment=self.environment,
                coordinates=self.environment.map.random_point(),
                available=True
            )
            for _ in range(self.num_clients)
        ]
        self.environment.add_clients(clients)
