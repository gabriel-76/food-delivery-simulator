from collections import defaultdict

import numpy as np

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.events.event_type import EventType
from src.main.statistic.metric import Metric


class TotalMetric(Metric):

    def __init__(self, environment: FoodDeliverySimpyEnv, table=False):
        super().__init__(environment)
        self.table = table

    def view(self, ax) -> None:
        print("TOTAL RESTAURANTS", len(self.environment.state.restaurants))
        print("TOTAL CLIENTS", len(self.environment.state.clients))
        print("TOTAL DRIVERS", len(self.environment.state.drivers))
        print("TOTAL ORDERS", len(self.environment.state.orders))

        labels = ['Restaurants', 'Clients', 'Drivers', 'Orders']
        values = [len(self.environment.state.restaurants), len(self.environment.state.clients),
                 len(self.environment.state.drivers), len(self.environment.state.orders)]

        ax.set_title('Total generated data')

        if self.table:
            ax.axis('tight')
            ax.axis('off')
            table_data = [[label, value] for label, value in zip(labels, values)]
            table = ax.table(cellText=table_data, colLabels=['Entities', 'Total'], cellLoc='center', loc='center')
            # table.auto_set_font_size(False)
            # table.set_fontsize(12)
            # table.scale(1.2, 1.2)
        else:
            ax.barh(labels, values, align='center')
            ax.set_xlabel('Total')
            ax.set_ylabel('Entities')



