from src.main.customer.customer import Customer
from src.main.actors.customer_actor import CustomerActor
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_generator import InitialGenerator


class InitialCustomerGenerator(InitialGenerator):
    def __init__(self, num_customers):
        self.num_customer = num_customers

    def run(self, env: FoodDeliverySimpyEnv):
        customer_actors = [
            CustomerActor(
                environment=env,
                customer=Customer(
                    coordinate=env.map.random_point(),
                    available=True
                )
            )
            for _ in range(self.num_customer)
        ]
        env.add_customers(customer_actors)
