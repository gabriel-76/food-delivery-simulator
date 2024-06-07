from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.client_generator_early import ClientGeneratorEarly
from src.main.generator.driver_generator_early import DriverGeneratorEarly
from src.main.generator.order_generator_early import OrderGeneratorEarly
from src.main.generator.restaurant_generator_eraly import RestaurantGeneratorEarly
from src.main.map.grid_map import GridMap
from src.main.optimizer.optimizer import Optimizer
from src.main.simulator.simulator import Simulator

NUM_CLIENTS = 10
NUM_RESTAURANTS = 2000
NUM_DRIVERS = 200
SIMULATION_TIME = 100


def simple():
    environment = FoodDeliveryEnvironment(GridMap(100))

    simulator = Simulator(
        environment=environment,
        generators=[
            ClientGeneratorEarly(environment, 10),
            RestaurantGeneratorEarly(environment, 10),
            DriverGeneratorEarly(environment, 10),
            OrderGeneratorEarly(environment, 10)
        ],
        optimizer=Optimizer(environment),
        debug=True,
        statistics=True
    )

    simulator.run(until=1440)


if __name__ == '__main__':
    simple()
