from collections import defaultdict

import numpy as np

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.events.event_type import EventType


class DelayMetric:
    def __init__(self, environment: FoodDeliverySimpyEnv):
        self.environment = environment

    def metric(self):
        events = list(filter(lambda env: env.event_type in [
            EventType.DRIVER_ACCEPTED_DELIVERY,
            EventType.DRIVER_DELIVERED_ORDER
        ], self.environment.events))
        # Dicionário para armazenar os tempos de cada evento por order_id
        order_events = defaultdict(dict)

        # Preenchendo o dicionário com os tempos dos eventos
        for event in events:
            order_id = event.order_id
            event_type = event.event_type
            time = event.time

            order_events[order_id][event_type] = time

        # Calculando a diferença de tempo para cada order_id
        time_differences = {}
        for order_id, times in order_events.items():
            if EventType.DRIVER_ACCEPTED_DELIVERY in times and EventType.DRIVER_DELIVERED_ORDER in times:
                time_differences[order_id] = times[EventType.DRIVER_DELIVERED_ORDER] - times[
                    EventType.DRIVER_ACCEPTED_DELIVERY]

        # # Mostrando os resultados
        # for order_id, time_difference in time_differences.items():
        #     print(f"Order ID: {order_id} - Time Difference: {time_difference}")

        p1 = np.percentile(list(time_differences.values()), 1)
        p10 = np.percentile(list(time_differences.values()), 10)
        p50 = np.percentile(list(time_differences.values()), 50)
        p90 = np.percentile(list(time_differences.values()), 90)
        p99 = np.percentile(list(time_differences.values()), 99)
        print(f"01th percentile: {p1}")
        print(f"10th percentile: {p10}")
        print(f"50th percentile: {p50}")
        print(f"90th percentile: {p90}")
        print(f"99th percentile: {p99}")
