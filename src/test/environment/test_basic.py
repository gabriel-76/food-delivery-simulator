import unittest

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_client_generator import TimeShiftClientGenerator
from src.main.generator.time_shift_driver_generator import TimeShiftDriverGenerator
from src.main.generator.time_shift_order_generator import TimeShiftOrderGenerator
from src.main.generator.time_shift_restaurant_generator import TimeShiftRestaurantGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.optimizer import Optimizer
from src.main.optimizer.random_driver_optimizer import RandomDriverOptimizer


class TestBasic(unittest.TestCase):

    def runTest(self):
        environment = FoodDeliveryEnvironment(
            map=GridMap(100),
            generators=[
                TimeShiftClientGenerator(lambda time: 3),
                TimeShiftRestaurantGenerator(lambda time: 3),
                TimeShiftDriverGenerator(lambda time: 10),
                TimeShiftOrderGenerator(lambda time: 2 * time)
            ],
            optimizer=RandomDriverOptimizer()
        )

        self.assertEqual(environment.state.drivers, [])

        environment.run(until=2)

        self.assertTrue(len(environment.events) > 0)
