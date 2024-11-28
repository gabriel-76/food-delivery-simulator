from typing import List

from matplotlib.ticker import FuncFormatter
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.statistic.metric import Metric


class DriverTimeWaitingForOrderMetric(Metric):
    def __init__(self, environment: FoodDeliverySimpyEnv):
        super().__init__(environment)

    def view(self, ax) -> None:
        drivers = self.environment.state.drivers
        
        ids = [driver.driver_id for driver in drivers]
        times_waiting_for_order: List[int] = [int(driver.time_waiting_for_order) for driver in drivers]

        print("\nTempo que cada motorista passou esperando pelo pedido no Estabelecimento:")
        for driver_id, time in zip(ids, times_waiting_for_order):
            print(f"Motorista {driver_id}: {time:.2f} minutos esperando pelo pedido")

        ax.barh(ids, times_waiting_for_order, color='blue')
        ax.set_xlabel('Time waiting for order')
        ax.set_ylabel('Drivers')
        ax.set_title('Time waiting for order per Driver')

        ax.set_yticks(ids)
        ax.set_yticklabels([str(int(driver_id)) for driver_id in ids])

        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}'))
