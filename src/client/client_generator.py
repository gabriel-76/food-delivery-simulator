from src.client.client import Client
from src.environment.food_delivery_environment import FoodDeliveryEnvironment


class ClientGenerator:
    def __init__(self, environment: FoodDeliveryEnvironment, maximum_clients_per_time):
        self.environment = environment
        self.maximum_clients_per_time = maximum_clients_per_time

    def clients_per_time(self):
        return [
            Client(
                environment=self.environment,
                coordinates=self.environment.map.random_point(),
                available=True
            )
            for _ in range(self.maximum_clients_per_time)
        ]

    def generation_rate(self):
        return 1

    def generate(self):
        while True:
            clients = self.clients_per_time()
            self.environment.add_clients(clients)
            yield self.environment.timeout(self.generation_rate())
