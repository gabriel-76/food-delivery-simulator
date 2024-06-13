from matplotlib import pyplot as plt

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.initial_client_generator import InitialClientGenerator
from src.main.generator.initial_driver_generator import InitialDriverGenerator
from src.main.generator.initial_order_generator import InitialOrderGenerator
from src.main.generator.initial_restaurant_generator import InitialRestaurantGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.random_driver_optimizer import RandomDriverOptimizer
from src.main.view.grid_view_matplotlib import GridViewMatplotlib


def main():
    environment = FoodDeliveryEnvironment(
        map=GridMap(100),
        generators=[
            InitialClientGenerator(10),
            InitialRestaurantGenerator(10),
            InitialDriverGenerator(10),
            InitialOrderGenerator(10)
        ],
        optimizer=RandomDriverOptimizer(),
        view=GridViewMatplotlib()
    )
    environment.run(100)


if __name__ == '__main__':
    main()
