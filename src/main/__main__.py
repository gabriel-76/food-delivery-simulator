from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_customer_generator import TimeShiftCustomerGenerator
from src.main.generator.time_shift_driver_generator import TimeShiftDriverGenerator
from src.main.generator.time_shift_establishment_generator import TimeShiftEstablishmentGenerator
from src.main.generator.time_shift_order_generator import TimeShiftOrderGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.nearest_driver_optimizer import NearestDriverOptimizer
from src.main.statistic.default_board import DefaultBoard
from src.main.statistic.delay_metric import DelayMetric
from src.main.statistic.distance_metric import DistanceMetric
from src.main.statistic.driver_status_metric import DriverStatusMetric
from src.main.statistic.order_curve_metric import OrderCurveMetric
from src.main.statistic.order_status_metric import OrderStatusMetric
from src.main.statistic.total_metric import TotalMetric


def main():
    environment = FoodDeliverySimpyEnv(
        map=GridMap(100),
        generators=[
            TimeShiftCustomerGenerator(lambda time: 3),
            TimeShiftEstablishmentGenerator(lambda time: 3),
            TimeShiftDriverGenerator(lambda time: 10),
            TimeShiftOrderGenerator(lambda time: time * 2 if time <= 100 else 1)
        ],
        optimizer=NearestDriverOptimizer(),
        # view=GridViewMatplotlib()
    )
    environment.run(until=200)
    # environment.log_events()

    custom_board = DefaultBoard(metrics=[
        OrderCurveMetric(environment),
        TotalMetric(environment),
        DistanceMetric(environment),
        DelayMetric(environment),
        DriverStatusMetric(environment),
        OrderStatusMetric(environment),
    ])
    custom_board.view()


if __name__ == '__main__':
    main()
