from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.client.client import Client

NUM_CLIENTS = 3000


class ClientGenerator:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def clients_generation_policy(self):
        return [Client(self.environment, f"client_{i}", ()) for i in range(NUM_CLIENTS)]
