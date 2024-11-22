from typing import List

from matplotlib.ticker import FuncFormatter
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.statistic.metric import Metric


class EstablishmentOrdersFulfilledMetric(Metric):
    def __init__(self, environment: FoodDeliverySimpyEnv):
        super().__init__(environment)

    def view(self, ax) -> None:
        establishments = self.environment.state.establishments

        ids = [establishment.establishment_id for establishment in establishments]
        orders_fulfilled: List[int] = [int(establishment.orders_fulfilled) for establishment in establishments]

        print("\nPedidos Atendidos por Estabelecimento:")
        for est_id, count in zip(ids, orders_fulfilled):
            print(f"Estabelecimento {est_id}: {count} pedidos atendidos")

        ax.barh(ids, orders_fulfilled, color='skyblue')
        ax.set_xlabel('Orders Fulfilled')
        ax.set_ylabel('Establishments')
        ax.set_title('Orders Fulfilled per Establishment')

        ax.set_yticks(ids)
        ax.set_yticklabels([str(int(driver_id)) for driver_id in ids])

        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}'))

        