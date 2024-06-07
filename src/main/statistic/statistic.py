from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np

from src.main.environment.food_delivery_environment import FoodDeliveryEnvironment
from src.main.events.event_type import EventType


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

        # self.orders_graph()
        # plt.show()

        events = filter(
            lambda event: event.event_type in [
                EventType.DRIVER_DELIVERED_ORDER,
                EventType.RESTAURANT_FINISHED_ORDER,
                EventType.CLIENT_PLACED_ORDER,
            ],
            self.environment.events.items
        )

        # Agrupar e contar os dados por status
        status_counts = defaultdict(lambda: defaultdict(int))
        for item in events:
            status_counts[item.event_type][item.time] += 1

        # Preparar os dados para plotar
        status_series = {}
        for status, times in status_counts.items():
            sorted_times = sorted(times.items())
            times, counts = zip(*sorted_times)
            status_series[status] = (times, counts)

        # Plotar os dados
        plt.figure(figsize=(30, 30))
        plt.figure()
        for status, (times, counts) in status_series.items():
            plt.plot(times, counts, label=status.name.lower())

        # Configurações do gráfico
        plt.xlabel('Tempo')
        plt.ylabel('Quantidade')
        plt.title('Quantidade por Status ao Longo do Tempo')
        plt.legend(title='Status')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(False)
        plt.show()

        # events = self.environment.orders
        #
        # # Agrupar e contar os dados por status
        # status_counts = defaultdict(lambda: defaultdict(int))
        # for item in events:
        #     status_counts[item.status][item.request_date] += 1
        #
        # # Preparar os dados para plotar
        # status_series = {}
        # for status, times in status_counts.items():
        #     sorted_times = sorted(times.items())
        #     times, counts = zip(*sorted_times)
        #     status_series[status] = (times, counts)
        #
        # # Plotar os dados
        # plt.figure(figsize=(30, 30))
        # plt.figure()
        # for status, (times, counts) in status_series.items():
        #     plt.plot(times, counts, label=status.name.lower())
        #
        # # Configurações do gráfico
        # plt.xlabel('Tempo')
        # plt.ylabel('Quantidade')
        # plt.title('Quantidade por Status ao Longo do Tempo')
        # plt.legend(title='Status')
        # plt.xticks(rotation=45)
        # plt.tight_layout()
        # plt.grid(False)
        # plt.show()


    def orders_graph(self):
        orders_time_counts = defaultdict(int)
        for order in self.environment.orders:
            orders_time_counts[order.request_date] += 1

        times = list(orders_time_counts.keys())
        counts = list(orders_time_counts.values())

        delivered_orders = filter(lambda event: event.event_type is EventType.DRIVER_DELIVERED_ORDER, self.environment.events.items)
        delivered_time_counts = defaultdict(int)
        for delivered_order in delivered_orders:
            delivered_time_counts[delivered_order.time] += 1

        # self.line_graph(times, counts)

        fig, ax = plt.subplots()
        ax.plot(times, counts, linewidth=2.0, label='Orders')
        ax.plot(list(delivered_time_counts.keys()), list(delivered_time_counts.values()), linewidth=2.0, label='Delivered')

        plt.xlabel('Tempo')
        plt.ylabel('Quantidade de Ordens')
        plt.title('Quantidade de Ordens Criadas ao Longo do Tempo')
        plt.legend()

    # def line_graph(self, x, y):
    #     # plot


