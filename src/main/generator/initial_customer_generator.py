from src.main.models.customer.customer import Customer
from src.main.environment.delivery_environment import DeliveryEnvironment
from src.main.generator.initial_generator import InitialGenerator


class InitialCustomerGenerator(InitialGenerator):
    def __init__(self, num_customers):
        self.num_customer = num_customers

    def run(self, env: DeliveryEnvironment):
        customers = [
            Customer(
                coordinate=env.map.random_point(),
                available=True
            )
            for _ in range(self.num_customer)
        ]
        env.add_customers(customers)
