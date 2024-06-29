from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.optimizer.optimizer import Optimizer
from src.main.models.route.route import Route


class FirstDriverOptimizer(Optimizer):
    def __init__(self, time_shift=1):
        super().__init__(time_shift=time_shift)

    def select_driver(self, env: FoodDeliverySimpyEnv, route: Route):
        drivers = env.available_drivers(route)
        # drivers = list(filter(lambda driver: driver.current_route is None or
        # driver.current_route.size() <= 1, drivers))
        return drivers[0] if len(drivers) > 0 else None
