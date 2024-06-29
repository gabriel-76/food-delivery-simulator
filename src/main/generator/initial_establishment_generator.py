from src.main.models.base import Dimensions
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.models.establishment.establishment import Establishment
from src.main.models.establishment.catalog import Catalog
from src.main.generator.initial_generator import InitialGenerator
from src.main.models.order import Item


class InitialEstablishmentGenerator(InitialGenerator):
    def __init__(self, num_establishments, use_estimate: bool = False):
        self.num_establishments = num_establishments
        self.use_estimate = use_estimate

    def run(self, env: FoodDeliverySimpyEnv):
        dimension = Dimensions(1, 1, 1, 1)
        catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
        establishments = [
            Establishment(
                coordinate=env.map.random_point(),
                available=True,
                catalog=catalog,
                use_estimate=self.use_estimate
            )
            for _ in range(self.num_establishments)
        ]
        env.add_establishments(establishments)
