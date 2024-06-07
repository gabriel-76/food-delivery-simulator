from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_client_generator import TimeShiftClientGenerator
from src.main.generator.initial_client_generator import InitialClientGenerator
from src.main.generator.initial_driver_generator import DriverGeneratorEarly
from src.main.generator.time_shift_order_generator import TimeShiftOrderGenerator
from src.main.generator.initial_order_generator import InitialOrderGenerator
from src.main.generator.initial_restaurant_generator import InitialRestaurantGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.optimizer import Optimizer
from src.main.simulator.simulator import Simulator
from src.main.statistic.statistic import Statistic

NUM_CLIENTS = 10
NUM_RESTAURANTS = 2000
NUM_DRIVERS = 200
SIMULATION_TIME = 100


def simple():
    environment = FoodDeliveryEnvironment(GridMap(100))

    simulator = Simulator(
        environment=environment,
        generators=[
            InitialClientGenerator(environment, 10),
            InitialRestaurantGenerator(environment, 10),
            DriverGeneratorEarly(environment, 10),
            # OrderGeneratorEarly(environment, 10),
            TimeShiftOrderGenerator(environment, 10)
        ],
        optimizer=Optimizer(environment),
        statistic=Statistic(environment),
        debug=False,
    )

    simulator.run(until=100)


if __name__ == '__main__':
    simple()
