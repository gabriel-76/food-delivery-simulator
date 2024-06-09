from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.generator.time_shift_client_generator import TimeShiftClientGenerator
from src.main.generator.time_shift_driver_generator import TimeShiftDriverGenerator
from src.main.generator.time_shift_order_generator import TimeShiftOrderGenerator
from src.main.generator.time_shift_restaurant_generator import TimeShiftRestaurantGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.optimizer import Optimizer
from src.main.statistic.statistic import Statistic


a = -4/225
b = 400


def main():
    environment = FoodDeliveryEnvironment(
        map=GridMap(100),
        generators=[
            TimeShiftClientGenerator(lambda time: 3),
            TimeShiftRestaurantGenerator(lambda time: 3),
            TimeShiftDriverGenerator(lambda time: 10),
            TimeShiftOrderGenerator(lambda time: max(2, a * pow(time-250, 2) + b))
        ],
        optimizer=Optimizer()
    )
    environment.run(until=2000)

    statistic = Statistic(environment)
    statistic.view()


if __name__ == '__main__':
    main()
