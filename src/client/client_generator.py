import random

from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.client.client import Client

NUM_CLIENTS = 3000


class ClientGenerator:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def generate(self):
        while True:
            clients = [Client(self.environment, f"client_{i}", (), True) for i in range(random.randrange(0, NUM_CLIENTS))]
            self.environment.add_clients(clients)
            yield self.environment.timeout(1)
