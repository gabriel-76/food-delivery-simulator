from src.client.client_generator import ClientGenerator
from src.driver.driver_generator import DriverGenerator
from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.map.map import Map
from src.optimizer.first_driver_optimizer import FirstDriverOptimizer
from src.optimizer.optimizer import Optimizer
from src.optimizer.random_driver_optimizer import RandomDriverOptimizer
from src.optimizer.nearest_driver_optimizer import NearestDriverOptimizer
from src.order.order_generator import OrderGenerator
from src.restaurant.restaurant_generator import RestaurantGenerator
from src.simulator.simulator import Simulator

SIMULATION_TIME = 100


def main():

    environment = FoodDeliveryEnvironment(Map(100))

    simulator = Simulator(
        environment,
        ClientGenerator(environment),
        RestaurantGenerator(environment),
        DriverGenerator(environment),
        OrderGenerator(environment),
        # Optimizer(environment),
        # FirstDriverOptimizer(environment),
        # RandomDriverOptimizer(environment),
        NearestDriverOptimizer(environment)
    )

    simulator.run(until=SIMULATION_TIME)
    # environment.debug()


if __name__ == '__main__':
    main()
