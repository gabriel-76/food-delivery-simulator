import unittest

from src.main.generator.client_generator import ClientGenerator
from src.main.generator.driver_generator import DriverGenerator
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.map.map import Map
from src.main.optimizer.nearest_driver_optimizer import NearestDriverOptimizer
from src.main.generator.order_generator import OrderGenerator
from src.main.generator.restaurant_generator import RestaurantGenerator
from src.main.simulator.simulator import Simulator


class TestSimulator(unittest.TestCase):

    def runTest(self):
        environment = FoodDeliveryEnvironment(Map(100))

        simulator = Simulator(
            environment,
            ClientGenerator(environment, 2),
            # RandomClientGenerator(environment, 0, NUM_CLIENTS),
            RestaurantGenerator(environment),
            DriverGenerator(environment),
            OrderGenerator(environment),
            # Optimizer(environment),
            # FirstDriverOptimizer(environment),
            # RandomDriverOptimizer(environment),
            NearestDriverOptimizer(environment)
        )

        self.assertEqual(environment.drivers, [])

        simulator.run(until=2)

        self.assertTrue(len(environment.events.items) > 0)