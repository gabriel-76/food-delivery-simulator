from src.main.client.client_generator import ClientGenerator
from src.main.driver.driver_generator import DriverGenerator
from src.main.driver.reactive_driver_generator import ReactiveDriverGenerator
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.map.map import Map
from src.main.optimizer.nearest_driver_optimizer import NearestDriverOptimizer
from src.main.optimizer.nop_optimizer import NopOptimizer
from src.main.order.order_generator import OrderGenerator
from src.main.restaurant.restaurant_generator import RestaurantGenerator
from src.main.simulator.simulator import Simulator

NUM_CLIENTS = 10
SIMULATION_TIME = 100


def main():

    environment = FoodDeliveryEnvironment(Map(100))

    simulator = Simulator(
        environment,
        ClientGenerator(environment, NUM_CLIENTS),
        # RandomClientGenerator(environment, 0, NUM_CLIENTS),
        RestaurantGenerator(environment),
        # DriverGenerator(environment),
        ReactiveDriverGenerator(environment),
        OrderGenerator(environment),
        # Optimizer(environment),
        # FirstDriverOptimizer(environment),
        # RandomDriverOptimizer(environment),
        # NearestDriverOptimizer(environment),
        NopOptimizer(environment),
        debug=True
    )

    simulator.run(until=SIMULATION_TIME)


if __name__ == '__main__':
    main()
