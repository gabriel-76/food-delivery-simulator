from src.main.client.client import Client
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator


class TimeShiftClientGenerator(TimeShiftGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, function, time_shift=1):
        super().__init__(environment, function, time_shift)

    def run(self):
        clients = [
            Client(
                environment=self.environment,
                coordinates=self.environment.map.random_point(),
                available=True
            )
            for _ in self.range()
        ]
        self.environment.add_clients(clients)
