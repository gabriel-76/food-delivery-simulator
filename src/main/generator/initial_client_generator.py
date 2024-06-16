from src.main.client.client import Client
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_generator import InitialGenerator


class InitialClientGenerator(InitialGenerator):
    def __init__(self, num_clients):
        self.num_clients = num_clients

    def run(self, env: FoodDeliverySimpyEnv):
        clients = [
            Client(
                environment=env,
                coordinates=env.map.random_point(),
                available=True
            )
            for _ in range(self.num_clients)
        ]
        env.add_clients(clients)
