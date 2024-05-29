from src.client.client_factory import ClientFactory
from src.driver.driver_factory import DriverFactory
from src.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.optimizer.optimizer import Optimizer
from src.order.order_factory import OrderFactory
from src.restaurant.restaurant_factory import RestaurantFactory
from src.simulator.simulator import Simulator

SIMULATION_TIME = 1000


def main():
    environment = FoodDeliveryEnvironment()
    optimizer = Optimizer(environment)
    order_factory = OrderFactory(environment)
    client_factory = ClientFactory(environment)
    restaurant_factory = RestaurantFactory(environment)
    driver_factory = DriverFactory(environment)
    simulator = Simulator(environment, optimizer, client_factory, restaurant_factory, driver_factory, order_factory)
    simulator.run()
    environment.run(until=SIMULATION_TIME)

    for order in environment.ready_orders.items:
        print(f"==============> order_{order.order_id}")
    print()


if __name__ == '__main__':
    main()
