from src.client.client_generator import ClientGenerator
from src.driver.driver_generator import DriverGenerator
from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.optimizer.optimizer import Optimizer
from src.order.order_generator import OrderGenerator
from src.restaurant.restaurant_generator import RestaurantGenerator
from src.simulator.simulator import Simulator

SIMULATION_TIME = 1000


def main():
    environment = FoodDeliveryEnvironment()
    simulator = Simulator(
        environment,
        ClientGenerator(environment),
        RestaurantGenerator(environment),
        DriverGenerator(environment),
        OrderGenerator(environment),
        Optimizer(environment)
    )
    simulator.run()
    environment.run(until=SIMULATION_TIME)

    for order in environment.ready_orders.items:
        print(f"==============> order_{order.order_id}")
    print()


if __name__ == '__main__':
    main()
