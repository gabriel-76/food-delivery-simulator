from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment


class Statistic:
    def __init__(self, environment: FoodDeliveryEnvironment):
        self.environment = environment

    def log(self):
        print()
        print("TOTAL RESTAURANTS", len(self.environment.restaurants))
        print("TOTAL CLIENTS", len(self.environment.clients))
        print("TOTAL DRIVERS", len(self.environment.drivers))
        print("TOTAL ORDERS", len(self.environment.orders))
        print()

        print("ORDERS")
        order_status_counts = defaultdict(int)
        for order in self.environment.orders:
            order_status_counts[order.status.name] += 1

        for status, count in order_status_counts.items():
            print(f"{status} {count}")

        print()

        print("DRIVERS")
        drivers_status_counts = defaultdict(int)
        for driver in self.environment.drivers:
            drivers_status_counts[driver.status.name] += 1

        for status, count in drivers_status_counts.items():
            print(f"{status} {count}")

        # self.environment.orders.sort(key=lambda x: x.status)
        #
        # for k, g in groupby(self.environment.orders, key=lambda order: order.status):
        #     print(k.name, len(list(g)))

        self.orders_graph()
        plt.show()


    def orders_graph(self):
        orders_time_counts = defaultdict(int)
        for order in self.environment.orders:
            orders_time_counts[order.request_date] += 1

        times = list(orders_time_counts.keys())
        counts = list(orders_time_counts.values())

        self.line_graph(times, counts)

    def line_graph(self, x, y):
        # plot
        fig, ax = plt.subplots()
        ax.plot(x, y, linewidth=2.0)
        plt.xlabel('Tempo')
        plt.ylabel('Quantidade de Ordens')
        plt.title('Quantidade de Ordens Criadas ao Longo do Tempo')
