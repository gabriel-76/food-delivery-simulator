from src.main.optimizer.optimizer_gym.optmizer_gym import OptimizerGym
from src.main.route.route import Route


class FirstDriverOptimizerGym(OptimizerGym):
    
    def select_driver(self, drivers, route: Route):
        # drivers = list(filter(lambda driver: driver.current_route is None or
        # driver.current_route.size() <= 1, drivers))
        
        # Retornando o index do primeiro motorista
        return 0 if len(drivers) > 0 else None
