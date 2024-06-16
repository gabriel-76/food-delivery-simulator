from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_driver_generator import InitialDriverGenerator
from src.main.generator.initial_restaurant_order_reate_generator import InitialRestaurantOrderRateGenerator
from src.main.generator.time_shift_order_restaurant_rate_generator import TimeShiftOrderRestaurantRateGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.random_driver_optimizer import RandomDriverOptimizer
from src.main.statistic.custom_board import CustomBoard
from src.main.statistic.driver_status_metric import DriverStatusMetric
from src.main.statistic.order_curve_metric import OrderCurveMetric
from src.main.statistic.order_status_metric import OrderStatusMetric


def run():
    environment = FoodDeliverySimpyEnv(
        map=GridMap(100),
        generators=[
            InitialRestaurantOrderRateGenerator(100),
            InitialDriverGenerator(20),
            TimeShiftOrderRestaurantRateGenerator(lambda time: 1),
        ],
        optimizer=RandomDriverOptimizer(use_estimate=True)
    )
    environment.run(100)

    custom_board = CustomBoard(metrics=[
        DriverStatusMetric(environment),
        OrderStatusMetric(environment),
        OrderCurveMetric(environment)
    ])
    custom_board.view()


if __name__ == '__main__':
    run()
