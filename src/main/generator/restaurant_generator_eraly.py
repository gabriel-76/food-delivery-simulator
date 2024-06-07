from src.main.base.dimensions import Dimensions
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.order.item import Item
from src.main.restaurant.catalog import Catalog
from src.main.restaurant.restaurant import Restaurant
from src.main.generator.restaurant_generator import RestaurantGenerator


class RestaurantGeneratorEarly(RestaurantGenerator):
    def __init__(self, environment: FoodDeliveryEnvironment, num_restaurants):
        super().__init__(environment)
        self.environment = environment
        self.num_restaurants = num_restaurants

    def generate(self):
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
        yield self.environment.timeout(1)
