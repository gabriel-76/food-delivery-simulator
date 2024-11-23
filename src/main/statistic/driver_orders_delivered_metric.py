from typing import List

from matplotlib.ticker import FuncFormatter
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.statistic.metric import Metric


class DriverOrdersDeliveredMetric(Metric):
    def __init__(self, environment: FoodDeliverySimpyEnv):
        super().__init__(environment)

    def view(self, ax) -> None:
        drivers = self.environment.state.drivers
        
        ids = [driver.driver_id for driver in drivers]
        orders_delivered: List[int] = [int(driver.orders_delivered) for driver in drivers]

        print("\nPedidos Entregues por Motorista:")
        for driver_id, count in zip(ids, orders_delivered):
            print(f"Motorista {driver_id}: {count} pedidos entregues")

        ax.barh(ids, orders_delivered, color='blue')
        ax.set_xlabel('Orders Delivered')
        ax.set_ylabel('Drivers')
        ax.set_title('Orders Delivered per Driver')

        ax.set_yticks(ids)
        ax.set_yticklabels([str(int(driver_id)) for driver_id in ids])

        ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x)}'))

        