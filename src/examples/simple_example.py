from src.main.environment.delivery_environment import DeliveryEnvironment
from src.main.generator.initial_customer_generator import InitialCustomerGenerator
from src.main.generator.initial_driver_generator import InitialDriverGenerator
from src.main.generator.initial_establishment_order_rate_generator import InitialEstablishmentOrderRateGenerator
from src.main.generator.initial_order_generator import InitialOrderGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.random_driver_optimizer import RandomDriverOptimizer
from src.main.view.grid_view_pygame import GridViewPygame


def run():
    environment = DeliveryEnvironment(
        map=GridMap(100),
        generators=[
            InitialEstablishmentOrderRateGenerator(1),
            InitialCustomerGenerator(10),
            InitialDriverGenerator(2),
            InitialOrderGenerator(30),
        ],
        optimizer=RandomDriverOptimizer(),
        view=GridViewPygame()
    )
    environment.run(200, render_mode='human')
    environment.log_events()


if __name__ == '__main__':
    run()
