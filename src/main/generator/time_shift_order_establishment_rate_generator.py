import random

from src.main.base.geometry import point_in_gauss_circle
from src.main.customer.customer import Customer
from src.main.actors.customer_actor import CustomerActor
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.order import Order


class TimeShiftOrderEstablishmentRateGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift=1):
        super().__init__(function, time_shift)
        self.hash_timeout = {}

    def process_establishment(self, env: FoodDeliverySimpyEnv, establishment):

        if establishment.establishment_id not in self.hash_timeout or self.hash_timeout[establishment.establishment_id] == env.now:

            customer = Customer(
                coordinate=point_in_gauss_circle(
                    establishment.coordinate,
                    establishment.operating_radius,
                    env.map.size
                ),
                available=True
            )

            customer_actor = CustomerActor(
                environment=env,
                customer=customer,
            )

            items = random.sample(establishment.catalog.items, 2)

            order = Order(customer, establishment, env.now, items)

            env.state.add_customers([customer])
            env.state.add_orders([order])

            customer_actor.place_order(order, establishment)

            timeout = round(random.expovariate(1 / establishment.order_request_time_rate))
            # print("generated in time", env.now, timeout)

            self.hash_timeout[establishment.establishment_id] = env.now + max(timeout, 1)

    def run(self, env: FoodDeliverySimpyEnv):
        for _ in self.range(env):
            for establishment in env.state.establishments:
                self.process_establishment(env, establishment)
