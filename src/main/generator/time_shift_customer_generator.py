from src.main.models.customer.customer import Customer
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_generator import TimeShiftGenerator


class TimeShiftCustomerGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift=1):
        super().__init__(function, time_shift)

    def run(self, env: FoodDeliverySimpyEnv):
        customer = [
            Customer(
                coordinate=env.map.random_point(),
                available=True
            )
            for _ in self.range(env)
        ]
        env.add_customers(customer)
