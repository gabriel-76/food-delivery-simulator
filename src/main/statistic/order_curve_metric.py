from collections import defaultdict

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.events.event_type import EventType
from src.main.statistic.metric import Metric


class OrderCurveMetric(Metric):
    def __init__(self, environment: FoodDeliverySimpyEnv):
        super().__init__(environment)

    def view(self, ax) -> None:
        events = filter(
            lambda event: event.event_type in [
                EventType.CUSTOMER_PLACED_ORDER,
                EventType.DRIVER_DELIVERED_ORDER,
                EventType.ESTABLISHMENT_FINISHED_ORDER,
            ],
            self.environment.events
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
        # plt.figure()
        for status, (times, counts) in status_series.items():
            ax.plot(times, counts, label=status.name.lower())

        # Configurações do gráfico
        ax.set_xlabel('Time')
        ax.set_ylabel('Number of orders')
        ax.set_title('Number of orders by state over time')
        ax.legend(title='Status')
        ax.grid(False)
        # plt.show()


