import simpy

from src.enviroment.food_delivery_environment import FoodDeliveryEnvironment
from src.simulator.simulator import Simulator

SIMULATION_TIME = 100000


def main():
    environment = FoodDeliveryEnvironment()
    simulator = Simulator(environment)
    simulator.run()
    environment.run(until=SIMULATION_TIME)

    for order in environment.ready_orders.items:
        print(f"==============> order_{order.order_id}")
    print()


if __name__ == '__main__':
    main()
