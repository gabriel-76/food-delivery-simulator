import random

from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.establishment.establishment import Establishment
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.order.item import Item
from src.main.establishment.catalog import Catalog
from src.main.actors.establishment_actor_order_rate import EstablishmentActorOrderRate


class TimeShiftEstablishmentOrderRateGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift, use_estimate: bool = False):
        super().__init__(function, time_shift)
        self.use_estimate = use_estimate

    def run(self, env: FoodDeliverySimpyEnv):
        dimension = Dimensions(1, 1, 1, 1)
        catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
        establishments = [
            Establishment(
                coordinate=env.map.random_point(),
                available=True,
                catalog=catalog,
                production_capacity=1,
                use_estimate=self.use_estimate,
                order_request_time_rate=random.randint(1, 10),
                order_production_time_rate=random.randint(1, 10),
                operating_radius=random.randint(10, 30)
            )
            for _ in self.range(env)
        ]
        env.add_establishments(establishments)
