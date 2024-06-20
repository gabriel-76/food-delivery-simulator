from src.main.cost.simple_cost_function import SimpleCostFunction
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_driver_generator import InitialDriverGenerator
from src.main.generator.initial_restaurant_order_reate_generator import InitialRestaurantOrderRateGenerator
from src.main.generator.time_shift_order_restaurant_rate_generator import TimeShiftOrderRestaurantRateGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.or_tools_optimizer import OrToolsOptimizer
from src.main.statistic.custom_board import CustomBoard
from src.main.statistic.delay_metric import DelayMetric
from src.main.statistic.distance_metric import DistanceMetric
from src.main.statistic.driver_status_metric import DriverStatusMetric
from src.main.statistic.order_curve_metric import OrderCurveMetric
from src.main.statistic.order_status_metric import OrderStatusMetric
from src.main.statistic.total_metric import TotalMetric
from src.main.view.grid_view_pygame import GridViewPygame


def run():
    environment = FoodDeliverySimpyEnv(
        map=GridMap(100),
        generators=[
            InitialRestaurantOrderRateGenerator(10),
            InitialDriverGenerator(10),
            TimeShiftOrderRestaurantRateGenerator(lambda time: 1 if time < 400 else 0),
        ],
        optimizer=OrToolsOptimizer(cost_function=SimpleCostFunction()),
        view=GridViewPygame()
    )
    environment.run(500, render_mode='human')

    custom_board = CustomBoard(metrics=[
        OrderCurveMetric(environment),
        TotalMetric(environment),
        DistanceMetric(environment),
        DelayMetric(environment),
        DriverStatusMetric(environment),
        OrderStatusMetric(environment),
    ])
    custom_board.view()


if __name__ == '__main__':
    run()
