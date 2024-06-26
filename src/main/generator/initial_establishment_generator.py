from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.establishment.establishment import Establishment
from src.main.generator.initial_generator import InitialGenerator
from src.main.order.item import Item
from src.main.establishment.catalog import Catalog
from src.main.actors.establishment_actor import EstablishmentActor


class InitialEstablishmentGenerator(InitialGenerator):
    def __init__(self, num_establishments, use_estimate: bool = False):
        self.num_establishments = num_establishments
        self.use_estimate = use_estimate

    def run(self, env: FoodDeliverySimpyEnv):
        dimension = Dimensions(1, 1, 1, 1)
        catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
        establishments = [
            EstablishmentActor(
                environment=env,
                establishment=Establishment(
                    coordinate=env.map.random_point(),
                    available=True,
                    catalog=catalog,
                    use_estimate=self.use_estimate
                )
            )
            for _ in range(self.num_establishments)
        ]
        env.add_establishments(establishments)
