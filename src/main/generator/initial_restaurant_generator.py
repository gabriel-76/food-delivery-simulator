from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.initial_generator import InitialGenerator
from src.main.order.item import Item
from src.main.restaurant.catalog import Catalog
from src.main.restaurant.restaurant import Restaurant


class InitialRestaurantGenerator(InitialGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, num_restaurants):
        super().__init__(environment)
        self.environment = environment
        self.num_restaurants = num_restaurants

    def run(self):
        dimension = Dimensions(1, 1, 1, 1)
        catalog = Catalog([Item(f"type_{i}", dimension, 4) for i in range(5)])
        restaurants = [
            Restaurant(
                environment=self.environment,
                coordinates=self.environment.map.random_point(),
                available=True,
                catalog=catalog
            )
            for _ in range(self.num_restaurants)
        ]
        self.environment.add_restaurants(restaurants)
