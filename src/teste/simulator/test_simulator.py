import unittest

from src.main.generator.time_shift_client_generator import TimeShiftClientGenerator
from src.main.generator.time_shift_driver_generator import TimeShiftDriverGenerator
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.map.map import Map
from src.main.optimizer.nearest_driver_optimizer import NearestDriverOptimizer
from src.main.generator.time_shift_order_generator import TimeShiftOrderGenerator
from src.main.generator.restaurant_generator import RestaurantGenerator
from src.main.simulator.simulator import Simulator


class TestSimulator(unittest.TestCase):

    def runTest(self):
        environment = FoodDeliveryEnvironment(Map(100))

        simulator = Simulator(
            environment,
            TimeShiftClientGenerator(environment, 2),
            # RandomClientGenerator(environment, 0, NUM_CLIENTS),
            RestaurantGenerator(environment),
            TimeShiftDriverGenerator(environment),
            TimeShiftOrderGenerator(environment),
            # Optimizer(environment),
            # FirstDriverOptimizer(environment),
            # RandomDriverOptimizer(environment),
            NearestDriverOptimizer(environment)
        )

        self.assertEqual(environment.drivers, [])

        simulator.run(until=2)

        self.assertTrue(len(environment.events.items) > 0)