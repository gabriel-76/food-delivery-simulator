import random

from src.main.generator.time_shift_client_generator import TimeShiftClientGenerator
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.client.client import Client


class RandomTimeShiftClientGenerator(TimeShiftClientGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, minimum_clients_per_time, maximum_clients_per_time):
        super().__init__(environment, maximum_clients_per_time)
        self.minimum_clients_per_time = minimum_clients_per_time

    def clients_per_time(self):
        return [
            Client(
                environment=self.environment,
                coordinates=self.environment.map.random_point(),
                available=True
            )
            for _ in range(random.randrange(self.minimum_clients_per_time, self.maximum_clients_per_time))
        ]
