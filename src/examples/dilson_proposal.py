from src.main.environment.delivery_environment import DeliveryEnvironment
from src.main.generator.initial_driver_generator import InitialDriverGenerator
from src.main.generator.initial_establishment_order_rate_generator import InitialEstablishmentOrderRateGenerator
from src.main.generator.time_shift_order_establishment_rate_generator import TimeShiftOrderEstablishmentRateGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.random_driver_optimizer import RandomDriverOptimizer
from src.main.statistic.custom_board import CustomBoard
from src.main.statistic.delay_metric import DelayMetric
from src.main.statistic.distance_metric import DistanceMetric
from src.main.statistic.driver_status_metric import DriverStatusMetric
from src.main.statistic.order_curve_metric import OrderCurveMetric
from src.main.statistic.order_status_metric import OrderStatusMetric
from src.main.statistic.total_metric import TotalMetric
from src.main.view.grid_view_pygame import GridViewPygame


def run():
    environment = DeliveryEnvironment(
        map=GridMap(100),
        generators=[
            InitialEstablishmentOrderRateGenerator(2),
            InitialDriverGenerator(20),
            TimeShiftOrderEstablishmentRateGenerator(lambda time: 1),
        ],
        optimizer=RandomDriverOptimizer(),
        view=GridViewPygame()
    )
    environment.run(100, render_mode='human')

    environment.log_events()

    # custom_board = CustomBoard(metrics=[
    #     OrderCurveMetric(environment),
    #     TotalMetric(environment),
    #     DistanceMetric(environment),
    #     DelayMetric(environment),
    #     DriverStatusMetric(environment),
    #     OrderStatusMetric(environment),
    # ])
    # custom_board.view()


if __name__ == '__main__':
    run()
