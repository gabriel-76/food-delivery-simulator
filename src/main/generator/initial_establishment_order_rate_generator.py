import random

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.models.commons.capacity import Capacity
from src.main.models.commons.dimension import Dimension
from src.main.models.commons.item import Item
from src.main.models.establishment.establishment import Establishment
from src.main.models.establishment.catalog import Catalog
from src.main.generator.initial_generator import InitialGenerator


class InitialEstablishmentOrderRateGenerator(InitialGenerator):
    def __init__(self, num_establishments, use_estimate: bool = False):
        self.num_establishments = num_establishments
        self.use_estimate = use_estimate

    def run(self, env: FoodDeliverySimpyEnv):
        dimension = Dimension(1, 1, 1, 1)
        catalog = Catalog([Item(dimension, 4) for _ in range(5)])
        capacity = Capacity(Dimension(100, 100, 100, 100))
        establishment = [
            Establishment(
                coordinate=env.map.random_point(),
                available=True,
                catalog=catalog,
                capacity=capacity,
                estimate=self.use_estimate,
                request_rate=random.uniform(5.0, 10.0),
                production_rate=random.uniform(5.0, 10.0),
                radius=random.randint(5, 30)
            )
            for _ in range(self.num_establishments)
        ]
        env.add_establishments(establishment)
