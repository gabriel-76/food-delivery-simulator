from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_client_generator import TimeShiftClientGenerator
from src.main.generator.time_shift_driver_generator import TimeShiftDriverGenerator
from src.main.generator.time_shift_order_generator import TimeShiftOrderGenerator
from src.main.generator.time_shift_restaurant_generator import TimeShiftRestaurantGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.random_driver_optimizer import RandomDriverOptimizer
from src.main.statistic.custom_board import CustomBoard
from src.main.statistic.driver_status_metric import DriverStatusMetric
from src.main.statistic.order_curve_metric import OrderCurveMetric
from src.main.statistic.order_status_metric import OrderStatusMetric

a = -4/225
b = 250
c = 400


def parable(time):
    return max(2, int(a * pow(time - b, 2) + c))


def run():
    environment = FoodDeliverySimpyEnv(
        map=GridMap(100),
        generators=[
            TimeShiftClientGenerator(lambda time: 3),
            TimeShiftRestaurantGenerator(lambda time: 3),
            TimeShiftDriverGenerator(lambda time: 3),
            TimeShiftOrderGenerator(lambda time: parable(time))
        ],
        optimizer=RandomDriverOptimizer(use_estimate=True)
    )
    environment.run(until=2000)

    custom_board = CustomBoard(metrics=[
        DriverStatusMetric(environment),
        OrderStatusMetric(environment),
        OrderCurveMetric(environment)
    ])
    custom_board.view()


if __name__ == '__main__':
    run()
