from typing import List

from matplotlib.ticker import FuncFormatter
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.statistic.metric import Metric


class DriverIdleTimeMetric(Metric):
    def __init__(self, environment: FoodDeliverySimpyEnv):
        super().__init__(environment)

    def view(self, ax) -> None:
        drivers = self.environment.state.drivers
        
        ids = [driver.driver_id for driver in drivers]
        idle_times: List[int] = [int(driver.idle_time) for driver in drivers]

        print("\nTempo Ocioso por Motorista:")
        for driver_id, idle_time in zip(ids, idle_times):
            print(f"Estabelecimento {driver_id}: {idle_time:.2f} minutos ocioso")

        ax.barh(ids, idle_times, color='green')
        ax.set_xlabel('Idle Time')
        ax.set_ylabel('Drivers')
        ax.set_title('Idle Time per Driver')

        ax.set_yticks(ids)
        ax.set_yticklabels([str(int(driver_id)) for driver_id in ids])

        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}'))

