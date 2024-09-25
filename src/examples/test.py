from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_customer_generator import InitialCustomerGenerator
from src.main.generator.initial_driver_generator import InitialDriverGenerator
from src.main.generator.initial_order_generator import InitialOrderGenerator
from src.main.generator.initial_establishment_generator import InitialEstablishmentGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.random_driver_optimizer import RandomDriverOptimizer
from src.main.statistic.custom_board import CustomBoard
from src.main.statistic.delay_metric import DelayMetric
from src.main.statistic.distance_metric import DistanceMetric
from src.main.statistic.driver_status_metric import DriverStatusMetric
from src.main.statistic.order_curve_metric import OrderCurveMetric
from src.main.statistic.order_status_metric import OrderStatusMetric
from src.main.statistic.total_metric import TotalMetric
from src.main.view.grid_view_matplotlib import GridViewMatplotlib


def main():
    environment = FoodDeliverySimpyEnv(
        map=GridMap(100),
        generators=[
            InitialCustomerGenerator(10),
            InitialEstablishmentGenerator(10),
            InitialDriverGenerator(10),
            InitialOrderGenerator(200)
        ],
        optimizer=RandomDriverOptimizer(),
        view=GridViewMatplotlib()
    )

    until = 100
    contar_eventos = 0
    while environment.peek() < until:
        print(environment.peek())
        # environment.step(render_mode='human')
        environment.step()
        if environment.dequeue_core_event():            
            print('Next client ready order event')
            contar_eventos += 1
    
    print(f'Contar eventos: {contar_eventos}')

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
    main()
