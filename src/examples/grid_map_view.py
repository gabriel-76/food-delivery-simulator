from matplotlib import pyplot as plt

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.initial_client_generator import InitialClientGenerator
from src.main.generator.initial_driver_generator import InitialDriverGenerator
from src.main.generator.initial_order_generator import InitialOrderGenerator
from src.main.generator.initial_restaurant_generator import InitialRestaurantGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.random_driver_optimizer import RandomDriverOptimizer
from src.main.statistic.grid_view import GridView


def main():
    environment = FoodDeliveryEnvironment(
        map=GridMap(100),
        generators=[
            InitialClientGenerator(10),
            InitialRestaurantGenerator(10),
            InitialDriverGenerator(10),
            InitialOrderGenerator(10)
        ],
        optimizer=RandomDriverOptimizer()
    )

    grid_view = GridView(environment)

    for util in range(1, 100):
        environment.run(until=util)
        grid_view.view()
        plt.pause(0.5)

    plt.ioff()
    plt.show()


if __name__ == '__main__':
    main()
