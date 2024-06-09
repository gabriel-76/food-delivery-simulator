from src.main.client.client import Client
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator


class TimeShiftClientGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift=1):
        super().__init__(function, time_shift)

    def run(self, env: FoodDeliveryEnvironment):
        clients = [
            Client(
                environment=env,
                coordinates=env.map.random_point(),
                available=True
            )
            for _ in self.range(env)
        ]
        env.add_clients(clients)
