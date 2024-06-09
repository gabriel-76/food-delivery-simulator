from src.main.driver.driver import Driver
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.optimizer.optimizer import Optimizer
from src.main.trip.trip import Trip


class NearestDriverOptimizer(Optimizer):

    def compare_distance(self, env: FoodDeliveryEnvironment, driver: Driver, trip: Trip):
        return env.map.distance(trip.routes[0].coordinates, driver.coordinates)

    def select_driver(self, env: FoodDeliveryEnvironment, trip: Trip):
        drivers = env.available_drivers(trip)
        # drivers = list(filter(lambda driver: driver.current_trip is None or driver.current_trip.size() <= 1, drivers))
        nearest_driver = min(drivers, key=lambda driver: self.compare_distance(env, driver, trip))
        return nearest_driver
