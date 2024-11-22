from typing import List

from matplotlib.ticker import FuncFormatter
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.statistic.metric import Metric


class EstablishmentIdleTimeMetric(Metric):
    def __init__(self, environment: FoodDeliverySimpyEnv):
        super().__init__(environment)

    def view(self, ax) -> None:
        establishments = self.environment.state.establishments

        ids = [establishment.establishment_id for establishment in establishments]
        idle_times: List[int] = [int(establishment.idle_time) for establishment in establishments]

        print("\nTempo Ocioso por Estabelecimento:")
        for est_id, idle_time in zip(ids, idle_times):
            print(f"Estabelecimento {est_id}: {idle_time:.2f} minutos ocioso")

        ax.barh(ids, idle_times, color='green')
        ax.set_xlabel('Idle Time')
        ax.set_ylabel('Establishments')
        ax.set_title('Idle Time per Establishment')

        ax.set_yticks(ids)
        ax.set_yticklabels([str(int(driver_id)) for driver_id in ids])

        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}'))

