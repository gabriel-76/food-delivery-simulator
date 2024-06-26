from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_customer_generator import TimeShiftCustomerGenerator
from src.main.generator.time_shift_driver_generator import TimeShiftDriverGenerator
from src.main.generator.time_shift_establishment_generator import TimeShiftEstablishmentGenerator
from src.main.generator.time_shift_order_generator import TimeShiftOrderGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.random_driver_optimizer import RandomDriverOptimizer
from src.main.statistic.custom_board import CustomBoard
from src.main.statistic.delay_metric import DelayMetric
from src.main.statistic.distance_metric import DistanceMetric
from src.main.statistic.driver_status_metric import DriverStatusMetric
from src.main.statistic.order_curve_metric import OrderCurveMetric
from src.main.statistic.order_status_metric import OrderStatusMetric
from src.main.statistic.total_metric import TotalMetric

a = -4/225
b = 250
c = 400


def parable(time):
    return max(2, int(a * pow(time - b, 2) + c))


def run():
    environment = FoodDeliverySimpyEnv(
        map=GridMap(100),
        generators=[
            TimeShiftCustomerGenerator(lambda time: 3),
            TimeShiftEstablishmentGenerator(lambda time: 3, use_estimate=True),
            TimeShiftDriverGenerator(lambda time: 3),
            TimeShiftOrderGenerator(lambda time: parable(time))
        ],
        optimizer=RandomDriverOptimizer()
    )
    environment.run(until=2000)

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
