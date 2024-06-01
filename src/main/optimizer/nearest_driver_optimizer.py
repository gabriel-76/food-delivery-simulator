from src.main.driver.driver import Driver
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.optimizer.optimizer import Optimizer
from src.main.order.order import Order


class NearestDriverOptimizer(Optimizer):
    def __init__(self, environment: FoodDeliveryEnvironment):
        super().__init__(environment)

    def compare_distance(self, driver: Driver, order: Order):
        collection_distance = self.environment.map.distance(driver.coordinates, order.restaurant.coordinates)
        delivery_distance = self.environment.map.distance(order.restaurant.coordinates, order.client.coordinates)
        total_distance = collection_distance + delivery_distance
        return total_distance

    def select_driver(self, order: Order):
        drivers = self.available_drivers(order)
        nearest_driver = min(drivers, key=lambda driver: self.compare_distance(driver, order))
        return nearest_driver
