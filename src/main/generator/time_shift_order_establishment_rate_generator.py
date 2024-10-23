import random

from src.main.base.geometry import point_in_gauss_circle
from src.main.customer.customer import Customer
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.order import Order


class TimeShiftOrderEstablishmentRateGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift=1, max_orders=None):
        super().__init__(function, time_shift)
        self.hash_timeout = {}
        self.max_orders = max_orders

    def process_establishment(self, env: FoodDeliverySimpyEnv, establishment):

        # TODO - Remover hash timeout e deixar o restaurante aceitar todos os pedidos

        if establishment.establishment_id not in self.hash_timeout or self.hash_timeout[establishment.establishment_id] <= env.now:

            customer = Customer(
                environment=env,
                coordinate=point_in_gauss_circle(
                    establishment.coordinate,
                    establishment.operating_radius,
                    env.map.size
                ),
                available=True,
                single_order=True
            )

            items = random.sample(establishment.catalog.items, 2)

            order = Order(customer, establishment, env.now, items)

            env.state.add_customers([customer])
            env.state.add_orders([order])

            customer.place_order(order, establishment)

            timeout = round(random.expovariate(1 / establishment.order_request_time_rate))
            # print("generated in time", env.now, timeout)

            self.hash_timeout[establishment.establishment_id] = env.now + max(timeout, 1)

    def run(self, env: FoodDeliverySimpyEnv):
        for _ in self.range(env):
            # Verificar se o número de pedidos foi atingido
            if self.max_orders and (env.state.get_length_orders() >= self.max_orders):
                return
            # for establishment in env.state.establishments:
            #     self.process_establishment(env, establishment)

            establishment = random.choice(env.state.establishments)
            self.process_establishment(env, establishment)
