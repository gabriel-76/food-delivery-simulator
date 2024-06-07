from src.main.generator.client_generator_early import ClientGeneratorEarly
from src.main.generator.driver_generator_early import DriverGeneratorEarly
from src.main.generator.reactive_driver_generator import ReactiveDriverGenerator
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.map.grid_map import GridMap
from src.main.map.map import Map
from src.main.optimizer.optimizer import Optimizer
from src.main.generator.order_generator_early import OrderGeneratorEarly
from src.main.generator.order_restaurant_rate_generator import OrderRestaurantRateGenerator
from src.main.generator.restaurant_generator_eraly import RestaurantGeneratorEarly
from src.main.generator.restaurant_order_rate_generator import RestaurantOrderRateGenerator
from src.main.simulator.simulator import Simulator

NUM_CLIENTS = 10
NUM_RESTAURANTS = 2000
NUM_DRIVERS = 200
SIMULATION_TIME = 100


def main():

    environment = FoodDeliveryEnvironment(Map(1000))

    simulator = Simulator(
        environment=environment,
        # client_generator=ClientGenerator(environment, NUM_CLIENTS),
        # client_generator=RandomClientGenerator(environment, 0, NUM_CLIENTS),
        # restaurant_generator=RestaurantGenerator(environment),
        restaurant_generator=RestaurantOrderRateGenerator(environment, NUM_RESTAURANTS),
        # driver_generator=DriverGenerator(environment),
        driver_generator=ReactiveDriverGenerator(environment, NUM_DRIVERS),
        # order_generator=OrderGenerator(environment),
        order_generator=OrderRestaurantRateGenerator(environment),
        # optimizer=Optimizer(environment),
        # FirstDriverOptimizer(environment),
        # RandomDriverOptimizer(environment),
        # NearestDriverOptimizer(environment),
        debug=True
    )

    simulator.run(until=SIMULATION_TIME)


def simple():

    environment = FoodDeliveryEnvironment(GridMap(100))

    simulator = Simulator(
        environment=environment,
        client_generator=ClientGeneratorEarly(environment, 1000),
        restaurant_generator=RestaurantGeneratorEarly(environment, 100),
        driver_generator=DriverGeneratorEarly(environment, 100),
        order_generator=OrderGeneratorEarly(environment, 1000),
        optimizer=Optimizer(environment),
        debug=True,
        statistics=True
    )

    simulator.run(until=1440)


if __name__ == '__main__':
    simple()
