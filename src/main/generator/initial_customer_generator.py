from src.main.actors.customer import Customer
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_generator import InitialGenerator


class InitialCustomerGenerator(InitialGenerator):
    def __init__(self, num_customers):
        self.num_customer = num_customers

    def run(self, env: FoodDeliverySimpyEnv):
        customers = [
            Customer(
                environment=env,
                coordinates=env.map.random_point(),
                available=True
            )
            for _ in range(self.num_customer)
        ]
        env.add_customers(customers)
