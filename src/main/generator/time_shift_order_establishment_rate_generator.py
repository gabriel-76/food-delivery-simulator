import random

from src.main.environment.delivery_environment import DeliveryEnvironment
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.models.customer.customer import Customer
from src.main.models.establishment.establishment import Establishment
from src.main.models.order.order import Order
from src.main.models.utils.geometry import point_in_gauss_circle


class TimeShiftOrderEstablishmentRateGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift=1):
        super().__init__(function, time_shift)
        self.hash_timeout = {}

    def process_establishment(self, env: DeliveryEnvironment, establishment: Establishment):

        if establishment.identifier not in self.hash_timeout or self.hash_timeout[establishment.identifier] == env.now:

            customer = Customer(
                coordinate=point_in_gauss_circle(
                    centroid=establishment.coordinate,
                    radius=establishment.radius,
                    inf_limit=0,
                    sup_limit=env.map.size
                ),
                available=True
            )

            items = random.sample(establishment.catalog.items, 2)

            order = Order(customer, establishment, items)

            env.place(order, customer, establishment)

            timeout = round(random.expovariate(1 / establishment.request_rate))
            # print("generated in time", env.now, timeout)

            self.hash_timeout[establishment.identifier] = env.now + max(timeout, 1)

    def run(self, env: DeliveryEnvironment):
        for _ in self.range(env):
            for establishment in env.state.establishments:
                self.process_establishment(env, establishment)
