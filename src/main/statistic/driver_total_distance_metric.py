from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.statistic.metric import Metric


class DriverTotalDistanceMetric(Metric):
    def __init__(self, environment: FoodDeliverySimpyEnv):
        super().__init__(environment)

    def view(self, ax) -> None:
        drivers = self.environment.state.drivers

        ids = [driver.driver_id for driver in drivers]
        total_distances = [driver.total_distance for driver in drivers]

        print("\nDistância Total Percorrida por Motorista:")
        for driver_id, distance in zip(ids, total_distances):
            print(f"Motorista {driver_id}: {distance:.2f} percorridos")
        
        ax.barh(ids, total_distances, color='red')
        ax.set_xlabel('Total Distance Traveled')
        ax.set_ylabel('Drivers')
        ax.set_title('Total Distance Traveled per Driver')
        
        ax.set_yticks(ids)
        ax.set_yticklabels([str(int(driver_id)) for driver_id in ids])