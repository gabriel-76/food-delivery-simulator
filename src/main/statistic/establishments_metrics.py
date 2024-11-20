from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.statistic.metric import Metric


class EstablishmentsMetrics(Metric):

    def __init__(self, environment: FoodDeliverySimpyEnv, table=False):
        super().__init__(environment)
        self.table = table

    def view(self, ax) -> None:
        establishments = self.environment.state.establishments

        print()
        print("ESTATÍSTICAS DOS ESTABELECIMENTOS:\n")
        for establishment in establishments:
            print(f"---------> Estabelecimento {establishment.establishment_id} <---------")
            print(f"Pedidos atendidos: {establishment.orders_fulfilled}")
            print(f"Máximo de pedidos em fila: {establishment.max_orders_in_queue}")
            print(f"Tempo ocioso: {establishment.idle_time}")
            print(f"Tempo ativo: {establishment.active_time}")
            print()
        