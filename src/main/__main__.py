import random

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_client_generator import TimeShiftClientGenerator
from src.main.generator.time_shift_driver_generator import TimeShiftDriverGenerator
from src.main.generator.time_shift_order_generator import TimeShiftOrderGenerator
from src.main.generator.time_shift_restaurant_generator import TimeShiftRestaurantGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.random_driver_optimizer import RandomDriverOptimizer
from src.main.statistic.statistic import Statistic


def main():
    environment = FoodDeliverySimpyEnv(
        map=GridMap(100),
        generators=[
            TimeShiftClientGenerator(lambda time: 3),
            TimeShiftRestaurantGenerator(lambda time: 3),
            TimeShiftDriverGenerator(lambda time: 10),
            TimeShiftOrderGenerator(lambda time: time * 2 if time <= 100 else 1)
        ],
        optimizer=RandomDriverOptimizer()
    )
    environment.run(until=200)
    environment.log_events()

    statistic = Statistic(environment)
    statistic.view()


if __name__ == '__main__':
    main()
