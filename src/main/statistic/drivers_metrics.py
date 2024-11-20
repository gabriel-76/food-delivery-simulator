from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.statistic.metric import Metric


class DriversMetrics(Metric):

    def __init__(self, environment: FoodDeliverySimpyEnv, table=False):
        super().__init__(environment)
        self.table = table

    def view(self, ax) -> None:
        drivers = self.environment.state.drivers

        print()
        print("ESTATÍSTICAS DOS MOTORISTAS:\n")
        for driver in drivers:
            print(f"---------> Motorista {driver.driver_id} <---------")
            print(f"Pedidos entregues: {driver.orders_delivered}")
            print(f"Distância total percorrida: {driver.total_distance}")
            print()
        