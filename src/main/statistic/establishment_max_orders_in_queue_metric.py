from typing import List

from matplotlib.ticker import FuncFormatter
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.statistic.metric import Metric


class EstablishmentMaxOrdersInQueueMetric(Metric):
    def __init__(self, environment: FoodDeliverySimpyEnv):
        super().__init__(environment)

    def view(self, ax) -> None:
        establishments = self.environment.state.establishments

        ids = [establishment.establishment_id for establishment in establishments]
        max_orders_in_queue: List[int] = [int(establishment.max_orders_in_queue) for establishment in establishments]

        print("\nMáximo de Pedidos na Fila por Estabelecimento:")
        for est_id, max_queue in zip(ids, max_orders_in_queue):
            print(f"Estabelecimento {est_id}: {max_queue} pedidos na fila")

        ax.barh(ids, max_orders_in_queue, color='orange')
        ax.set_xlabel('Max Orders in Queue')
        ax.set_ylabel('Establishments')
        ax.set_title('Max Orders in Queue per Establishment')

        ax.set_yticks(ids)
        ax.set_yticklabels([str(int(driver_id)) for driver_id in ids])

        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}'))

