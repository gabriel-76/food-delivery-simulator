import numpy as np

from src.main.statistic.driver_idle_time_metric import DriverIdleTimeMetric
from src.main.statistic.driver_orders_delivered_metric import DriverOrdersDeliveredMetric
from src.main.statistic.driver_time_waiting_for_order_metric import DriverTimeWaitingForOrderMetric
from src.main.statistic.driver_total_distance_metric import DriverTotalDistanceMetric
from src.main.statistic.establishment_active_time_metric import EstablishmentActiveTimeMetric
from src.main.statistic.establishment_idle_time_metric import EstablishmentIdleTimeMetric
from src.main.statistic.establishment_max_orders_in_queue_metric import EstablishmentMaxOrdersInQueueMetric
from src.main.statistic.establishment_orders_fulfilled_metric import EstablishmentOrdersFulfilledMetric
from src.main.statistic.summarized_data_board import SummarizedDataBoard


DIR_PATH = "./data/200_runs_with_all_agents/ppo_agent_trained_13000000/"
NUM_DRIVERS = 10
NUM_ESTABLISHMENTS = 10

def main():
    dados = np.load(DIR_PATH + "metrics_Data.npz", allow_pickle=True)
    
    total_rewards = dados["total_rewards"]
    T = dados["statistics"]  # Isso retorna um array do NumPy

    # Se for um array contendo um único dicionário, extraia o dicionário
    statistics = None
    if isinstance(T, np.ndarray) and T.dtype == object:
        statistics = T.item()  # Converte o array do NumPy em um dicionário Python

    # Calculando a média dos valores de recompensa
    sum_rewards_mean = sum(total_rewards) / len(total_rewards)

    custom_board = SummarizedDataBoard(metrics=[
        EstablishmentOrdersFulfilledMetric(None, establishments_statistics=statistics["establishments"]),
        EstablishmentMaxOrdersInQueueMetric(None, establishments_statistics=statistics["establishments"]),
        EstablishmentActiveTimeMetric(None, establishments_statistics=statistics["establishments"]),
        EstablishmentIdleTimeMetric(None, establishments_statistics=statistics["establishments"]),
        DriverOrdersDeliveredMetric(None, drivers_statistics=statistics["drivers"]),
        DriverTotalDistanceMetric(None, drivers_statistics=statistics["drivers"]),
        DriverIdleTimeMetric(None, drivers_statistics=statistics["drivers"]),
        DriverTimeWaitingForOrderMetric(None, drivers_statistics=statistics["drivers"])
    ],
        num_drivers=NUM_DRIVERS,
        num_establishments=NUM_ESTABLISHMENTS,
        sum_reward=sum_rewards_mean,
        save_figs=True,
        dir_path=DIR_PATH,
        use_total_mean=True,
        use_tkinter=False
    )
    custom_board.view()


if __name__ == '__main__':
    main()
