from src.main.client.client import Client
from src.main.client.client_generator import ClientGenerator
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment


class ClientGeneratorEarly(ClientGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, num_clients):
        super().__init__(environment, num_clients)
        self.environment = environment
        self.num_clients = num_clients

    def clients_per_time(self):
        return [
            Client(
                environment=self.environment,
                coordinates=self.environment.map.random_point(),
                available=True
            )
            for _ in range(self.num_clients)
        ]

    def generate(self):
        clients = self.clients_per_time()
        self.environment.add_clients(clients)
        yield self.environment.timeout(1)
