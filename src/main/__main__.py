from src.main.coast.simple_cost_function import SimpleCostFunction
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.time_shift_client_generator import TimeShiftClientGenerator
from src.main.generator.time_shift_driver_generator import TimeShiftDriverGenerator
from src.main.generator.time_shift_order_generator import TimeShiftOrderGenerator
from src.main.generator.time_shift_restaurant_generator import TimeShiftRestaurantGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.nearest_driver_optimizer import NearestDriverOptimizer
from src.main.statistic.custom_board import CustomBoard
from src.main.statistic.delay_metric import DelayMetric
from src.main.statistic.distance_metric import DistanceMetric
from src.main.statistic.driver_status_metric import DriverStatusMetric
from src.main.statistic.order_curve_metric import OrderCurveMetric
from src.main.statistic.order_status_metric import OrderStatusMetric


def main():
    environment = FoodDeliverySimpyEnv(
        map=GridMap(100),
        generators=[
            TimeShiftClientGenerator(lambda time: 3),
            TimeShiftRestaurantGenerator(lambda time: 3),
            TimeShiftDriverGenerator(lambda time: 10),
            TimeShiftOrderGenerator(lambda time: time * 2 if time <= 100 else 1)
        ],
        optimizer=NearestDriverOptimizer(SimpleCostFunction()),
        # view=GridViewMatplotlib()
    )
    environment.run(until=200)
    # environment.log_events()

    delay_metric = DelayMetric(environment)
    delay_metric.metric()

    print()

    distance_metric = DistanceMetric(environment)
    distance_metric.metric()

    print()

    custom_board = CustomBoard(metrics=[
        DriverStatusMetric(environment),
        OrderStatusMetric(environment),
        OrderCurveMetric(environment)
    ])
    custom_board.view()


if __name__ == '__main__':
    main()
