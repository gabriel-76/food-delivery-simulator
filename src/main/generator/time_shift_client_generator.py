from src.main.client.client import Client
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator


class TimeShiftClientGenerator(TimeShiftGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, num_clients, time_shift=1):
        super().__init__(environment, time_shift)
        self.maximum_clients_per_time = num_clients

    def run(self):
        clients = [
            Client(
                environment=self.environment,
                coordinates=self.environment.map.random_point(),
                available=True
            )
            for _ in range(self.maximum_clients_per_time)
        ]
        self.environment.add_clients(clients)
