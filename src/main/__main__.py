from src.main.client.client_generator import ClientGenerator
from src.main.driver.driver_generator import DriverGenerator
from src.main.driver.reactive_driver_generator import ReactiveDriverGenerator
from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.map.map import Map
from src.main.optimizer.nearest_driver_optimizer import NearestDriverOptimizer
from src.main.optimizer.optimizer import Optimizer
from src.main.order.order_generator import OrderGenerator
from src.main.order.order_restaurant_rate_generator import OrderRestaurantRateGenerator
from src.main.restaurant.restaurant_generator import RestaurantGenerator
from src.main.restaurant.restaurant_order_rate_generator import RestaurantOrderRateGenerator
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


if __name__ == '__main__':
    main()
