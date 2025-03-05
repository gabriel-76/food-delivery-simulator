from abc import ABC, abstractmethod
from typing import List

import numpy as np

from src.main.driver.driver import Driver
from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv
from src.main.optimizer.optimizer import Optimizer
from src.main.order.order import Order
from src.main.route.delivery_route_segment import DeliveryRouteSegment
from src.main.route.pickup_route_segment import PickupRouteSegment
from src.main.route.route import Route


class OptimizerGym(Optimizer, ABC):

    def __init__(self, environment: FoodDeliveryGymEnv):
        self.gym_env = environment
        self.state = None
        self.done = False
        self.truncated = False

    def initialize(self, seed: int | None = None):
        self.reset_env(seed=seed)
        self.gym_env.reset_statistics()

    def reset_env(self, seed: int | None = None):
        self.state, info = self.gym_env.reset(seed=seed)
        self.done = False
        self.truncated = False

    @abstractmethod
    def select_driver(self, obs: dict, drivers: List[Driver], route: Route):
        pass
    
    def assign_driver_to_order(self, obs: dict, order: Order):
        segment_pickup = PickupRouteSegment(order)
        segment_delivery = DeliveryRouteSegment(order)
        route = Route(self.gym_env.get_simpy_env(), [segment_pickup, segment_delivery])

        drivers = self.gym_env.get_drivers()

        return self.select_driver(obs, drivers, route)

    def run(self):
        sum = 0
        while not (self.done or self.truncated):
            action = self.assign_driver_to_order(self.state, self.gym_env.get_last_order())
            self.state, reward, self.done, self.truncated, info = self.gym_env.step(action)
            sum += reward

            print(f"State: {self.state}, Reward: {reward}, Done: {self.done}, Truncated: {self.truncated}")

        print(f"\n\n\nTotal reward: {sum}")
        print(f"Final Time  Step: {info['info']}")

        return {
            "final_state": self.state,
            "final_reward": reward,
            "done": self.done,
            "truncated": self.truncated,
            "sum_reward": sum,
            "info": info,
        }
    
    def show_statistcs_board(self):
        self.gym_env.show_statistcs_board()
    
    def show_mean_statistic_board(self):
        self.gym_env.show_total_mean_statistics_board()
    
    @abstractmethod
    def get_title(self):
        pass

    def get_description(self, results_file, num_runs: int, seed: int | None = None):
        results_file.write("-------------------> " + self.get_title() + " <-------------------\n\n")

        results_file.write("---> Configurações Gerais:\n")
        results_file.write(f"Número de execuções: {num_runs}\n")
        results_file.write(f"Seed de números aleatórios: {seed}\n")
        results_file.write("\n---> Configurações do Cenário do Ambiente: ")
        results_file.write(self.gym_env.get_description())
        results_file.write("\n\n")
    
    def format_statistics(self, statistics: dict):
        result = ""
        
        # Formata os dados para estabelecimentos
        if 'establishments' in statistics:
            result += "Establishments:\n"
            for establishment_id, stats in statistics['establishments'].items():
                result += f"  Establishment {establishment_id}:\n"
                for key, value in stats.items():
                    result += f"    {key.replace('_', ' ').title()}:\n"
                    for stat, stat_value in value.items():
                        result += f"      {stat.title()}: {stat_value}\n"
                result += "\n"
        
        # Formata os dados para motoristas
        if 'drivers' in statistics:
            result += "Drivers:\n"
            for driver_id, stats in statistics['drivers'].items():
                result += f"  Driver {driver_id}:\n"
                for key, value in stats.items():
                    result += f"    {key.replace('_', ' ').title()}:\n"
                    for stat, stat_value in value.items():
                        result += f"      {stat.title()}: {stat_value}\n"
                result += "\n"
        
        return result

    def run_simulations(self, num_runs: int, dir_path: str, seed: int | None = None):
        self.initialize(seed=seed)
        file_path = dir_path + "results.txt"

        total_rewards = []
        with open(file_path, "w", encoding="utf-8") as results_file:
            self.get_description(results_file, num_runs, seed)
            results_file.write("---> Registro de execuções:\n")
            for i in range(num_runs):
                print(f"Run {i + 1}")

                resultado = self.run()

                self.gym_env.register_statatistic_data()

                sum_reward = resultado["sum_reward"]
                self.gym_env.show_statistcs_board(sum_reward=sum_reward, dir_path=dir_path)
                total_rewards.append(sum_reward)

                results_file.write(f"Execução {i + 1}: Soma das Recompensas = {sum_reward}\n")

                self.reset_env()

            avg_reward = sum(total_rewards) / num_runs
            results_file.write(f"\n---> Média das somas das recompensas: {avg_reward:.2f}\n")
            statistics = self.gym_env.get_statistics()
            results_file.write(f"\n---> Estatísticas Finais:\n")
            results_file.write(f"{self.format_statistics(statistics)}")
            self.gym_env.show_total_mean_statistics_board(sum_rewards_mean=avg_reward, dir_path=dir_path)

            self.save_metrics_to_file(total_rewards, statistics, dir_path)
        
        print(f"Resultados salvos em " + file_path)

    def save_metrics_to_file(self, total_rewards: list, statistics: dict, dir_path: str = "./", file_name: str = "metrics_data.npz"):
        file_path = dir_path + file_name
        np.savez_compressed(file_path, total_rewards=total_rewards, statistics=statistics)