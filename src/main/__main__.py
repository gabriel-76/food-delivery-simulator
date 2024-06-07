import random

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_client_generator import TimeShiftClientGenerator
from src.main.generator.initial_client_generator import InitialClientGenerator
from src.main.generator.initial_driver_generator import InitialDriverGenerator
from src.main.generator.time_shift_driver_generator import TimeShiftDriverGenerator
from src.main.generator.time_shift_order_generator import TimeShiftOrderGenerator
from src.main.generator.initial_order_generator import InitialOrderGenerator
from src.main.generator.initial_restaurant_generator import InitialRestaurantGenerator
from src.main.generator.time_shift_restaurant_generator import TimeShiftRestaurantGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.optimizer import Optimizer
from src.main.simulator.simulator import Simulator
from src.main.statistic.statistic import Statistic

NUM_CLIENTS = 10
NUM_RESTAURANTS = 2000
NUM_DRIVERS = 200
SIMULATION_TIME = 100


def initial():
    environment = FoodDeliveryEnvironment(GridMap(100))

    simulator = Simulator(
        environment=environment,
        generators=[
            InitialClientGenerator(environment, 10),
            InitialRestaurantGenerator(environment, 10),
            InitialDriverGenerator(environment, 10),
            InitialOrderGenerator(environment, 10),
        ],
        optimizer=Optimizer(environment),
        statistic=Statistic(environment),
        debug=False,
    )

    simulator.run(until=100)


def time_shift():
    environment = FoodDeliveryEnvironment(GridMap(100))

    simulator = Simulator(
        environment=environment,
        generators=[
            TimeShiftClientGenerator(environment, lambda time: 3),
            TimeShiftRestaurantGenerator(environment, lambda time: 3),
            TimeShiftDriverGenerator(environment, lambda time: 10),
            TimeShiftOrderGenerator(environment, lambda time: 2 * time)
        ],
        optimizer=Optimizer(environment),
        statistic=Statistic(environment),
        debug=False,
    )

    simulator.run(until=100)


if __name__ == '__main__':
    # initial()
    time_shift()
