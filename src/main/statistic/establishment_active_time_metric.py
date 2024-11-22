from typing import List

from matplotlib.ticker import FuncFormatter
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.statistic.metric import Metric


class EstablishmentActiveTimeMetric(Metric):
    def __init__(self, environment: FoodDeliverySimpyEnv):
        super().__init__(environment)

    def view(self, ax) -> None:
        establishments = self.environment.state.establishments

        ids = [establishment.establishment_id for establishment in establishments]
        active_times: List[int] = [int(establishment.active_time) for establishment in establishments]

        print("\nTempo Ativo por Estabelecimento:")
        for est_id, active_time in zip(ids, active_times):
            print(f"Estabelecimento {est_id}: {active_time:.2f} minutos ativo")

        ax.barh(ids, active_times, color='purple')
        ax.set_xlabel('Active Time')
        ax.set_ylabel('Establishments')
        ax.set_title('Active Time per Establishment')

        ax.set_yticks(ids)
        ax.set_yticklabels([str(int(driver_id)) for driver_id in ids])

        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}'))

