import random

import numpy as np

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_generator import InitialGenerator
from src.main.order.item import Item
from src.main.establishment.catalog import Catalog
from src.main.establishment.establishment_order_rate import EstablishmentOrderRate


class InitialEstablishmentOrderRateGenerator(InitialGenerator):
    def __init__(self, num_establishments, use_estimate: bool = False):
        self.num_establishments = num_establishments
        self.use_estimate = use_estimate

    def run(self, env: FoodDeliverySimpyEnv):
        dimension = Dimensions(1, 1, 1, 1)
        catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
        establishment = [
            EstablishmentOrderRate(
                environment=env,
                coordinate=env.map.random_point(),
                available=True,
                catalog=catalog,
                production_capacity=np.inf,
                use_estimate=self.use_estimate,
                order_request_time_rate=random.uniform(5.0, 10.0),
                order_production_time_rate=random.uniform(5.0, 10.0),
                operating_radius=random.randint(5, 30),
            )
            for _ in range(self.num_establishments)
        ]
        env.add_establishments(establishment)
