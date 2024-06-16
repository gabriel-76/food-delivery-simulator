from collections import defaultdict

import numpy as np

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.events.event_type import EventType


class DistanceMetric:

    def __init__(self, environment: FoodDeliverySimpyEnv):
        self.environment = environment

    def metric(self):
        events = list(filter(lambda env: env.event_type in [
            EventType.DRIVER_COLLECTING_ORDER,
            EventType.DRIVER_DELIVERING_ORDER,
            EventType.DRIVER_COLLECTED_ORDER,
            EventType.DRIVER_DELIVERED_ORDER
        ], self.environment.events))

        # events = list(filter(
        #     lambda env: (hasattr(env, "distance") and env.distance > 0) or not hasattr(env, "distance"),
        #     events
        # ))

        # Dicionário para armazenar os tempos de cada evento por order_id
        driver_events = defaultdict(dict)

        # Preenchendo o dicionário com os tempos dos eventos
        for event in events:
            driver_id = event.driver_id
            order_id = event.order_id
            event_type = event.event_type
            distance = 0
            if hasattr(event, "distance"):
                distance = event.distance

            driver_events[(driver_id, order_id)][event_type] = distance

        # Calculando a diferença de tempo para cada order_id
        distances = {}
        for (driver_id, order_id), total_distances in driver_events.items():
            if EventType.DRIVER_COLLECTING_ORDER in total_distances and EventType.DRIVER_COLLECTED_ORDER in total_distances:
                if driver_id in distances:
                    distances[driver_id] += total_distances[EventType.DRIVER_COLLECTING_ORDER]
                else:
                    distances[driver_id] = total_distances[EventType.DRIVER_COLLECTING_ORDER]
            if EventType.DRIVER_DELIVERING_ORDER in total_distances and EventType.DRIVER_DELIVERED_ORDER in total_distances:
                if driver_id in distances:
                    distances[driver_id] += total_distances[EventType.DRIVER_DELIVERING_ORDER]
                else:
                    distances[driver_id] = total_distances[EventType.DRIVER_DELIVERING_ORDER]

        # # Mostrando os resultados
        # for driver_id, total_distance in distances.items():
        #     driver = next((d for d in self.environment.state.drivers if d.driver_id == driver_id))
        #     print(f"Driver ID: {driver_id} - Total Distance: {total_distance} {driver.total_distance} {total_distance > driver.total_distance}")

        distances = distances.values()

        min_distance = min(distances)
        p1 = np.percentile(list(distances), 1)
        p10 = np.percentile(list(distances), 10)
        p50 = np.percentile(list(distances), 50)
        p90 = np.percentile(list(distances), 90)
        p95 = np.percentile(list(distances), 95)
        p99 = np.percentile(list(distances), 99)
        max_distance = max(distances)

        print(f"Min distance: {min_distance}")
        print(f"01th percentile: {p1}")
        print(f"10th percentile: {p10}")
        print(f"50th percentile: {p50}")
        print(f"90th percentile: {p90}")
        print(f"95th percentile: {p95}")
        print(f"99th percentile: {p99}")
        print(f"Max distance: {max_distance}")
