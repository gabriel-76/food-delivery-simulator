from src.main.driver.driver import Driver
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.optimizer.optimizer import Optimizer
from src.main.trip.trip import Trip


class NearestDriverOptimizer(Optimizer):
    def __init__(self, use_estimate=False, time_shift=1):
        super().__init__(use_estimate=use_estimate, time_shift=time_shift)

    def compare_distance(self, env: FoodDeliverySimpyEnv, driver: Driver, trip: Trip):
        return env.map.distance(trip.routes[0].coordinates, driver.coordinates)

    def select_driver(self, env: FoodDeliverySimpyEnv, trip: Trip):
        drivers = env.available_drivers(trip)
        # drivers = list(filter(lambda driver: driver.current_trip is None or driver.current_trip.size() <= 1, drivers))
        nearest_driver = min(drivers, key=lambda driver: self.compare_distance(env, driver, trip))
        return nearest_driver
