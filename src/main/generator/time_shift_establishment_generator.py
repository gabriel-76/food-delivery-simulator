from src.main.models.base import Dimensions
from src.main.environment.delivery_environment import DeliveryEnvironment
from src.main.models.establishment.establishment import Establishment
from src.main.models.establishment.catalog import Catalog
from src.main.generator.time_shift_generator import TimeShiftGenerator
from src.main.models.order import Item


class TimeShiftEstablishmentGenerator(TimeShiftGenerator):
    def __init__(self, function, time_shift=1, use_estimate: bool = False):
        super().__init__(function, time_shift)
        self.use_estimate = use_estimate

    def run(self, env: DeliveryEnvironment):
        dimension = Dimensions(1, 1, 1, 1)
        catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
        establishments = [
            Establishment(
                coordinate=env.map.random_point(),
                available=True,
                catalog=catalog,
                use_estimate=self.use_estimate
            )
            for _ in self.range(env)
        ]
        env.add_establishments(establishments)
