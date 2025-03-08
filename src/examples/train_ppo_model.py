import os
import sys
import time
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import EvalCallback

from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv

NUM_DRIVERS = 10
NUM_ORDERS = 12*24  # 12 pedidos por hora durante 24 horas
NUM_ESTABLISHMENTS = 10
NUM_COSTUMERS = NUM_ORDERS
GRID_MAP_SIZE = 50  # Tamanho do grid 50x50
REWARD_OBJECTIVE = 1
MAX_TIME_STEP = 60*24*2  # 2 dias
FUNCTION = lambda time: 2  # 2 pedidos de 10 em 10 minutos
LAMBDA_CODE = "lambda time: 2"
TIME_SHIFT = 10

# Variáveis para criação dos Motoristas
VEL_DRIVERS = [3, 5]

# Variáveis para criação dos Estabelecimentos
PREPARE_TIME = [20, 60]
OPERATING_RADIUS = [5, 30]
PRODUCTION_CAPACITY = [4, 4]

# Variável que controla quando o motorista deve ser alocado
PERCENTAGE_ALLOCATION_DRIVER = 0.7

NORMALIZE = True
SEED = 101010

# Escolha se deseja salvar o log em um arquivo
SAVE_LOG_TO_FILE = False

DIR_PATH = "./data/ppo_training/6000000 eps/"

# Verificar e criar os diretórios necessários
os.makedirs(DIR_PATH + "logs/", exist_ok=True)
os.makedirs(DIR_PATH + "best_model/", exist_ok=True)
os.makedirs(DIR_PATH + "ppo_tensorboard/", exist_ok=True)

if SAVE_LOG_TO_FILE:
    log_file = open(DIR_PATH + "log.txt", "w", encoding="utf-8")
    sys.stdout = log_file
    sys.stderr = log_file

def main():
    try:
        # Criando o ambiente de treinamento
        gym_env = FoodDeliveryGymEnv(
            num_drivers=NUM_DRIVERS,
            num_establishments=NUM_ESTABLISHMENTS,
            num_orders=NUM_ORDERS,
            num_costumers=NUM_COSTUMERS,
            grid_map_size=GRID_MAP_SIZE,
            vel_drivers=VEL_DRIVERS,
            prepare_time=PREPARE_TIME,
            operating_radius=OPERATING_RADIUS,
            production_capacity=PRODUCTION_CAPACITY,
            percentage_allocation_driver=PERCENTAGE_ALLOCATION_DRIVER,
            use_estimate=True,
            desconsider_capacity=True,
            max_time_step=MAX_TIME_STEP,
            reward_objective=REWARD_OBJECTIVE,
            function=FUNCTION,
            lambda_code=LAMBDA_CODE,
            time_shift=TIME_SHIFT,
            normalize=NORMALIZE,
        )

        # Verificar se o ambiente está implementado corretamente
        check_env(gym_env, warn=True)

        # Monitorando o ambiente de treinamento
        gym_env = Monitor(gym_env, DIR_PATH + "logs/")
        env = DummyVecEnv([lambda: gym_env])

        # Criando o ambiente de avaliação separado (sem Monitor)
        eval_env = DummyVecEnv([lambda: FoodDeliveryGymEnv(
            num_drivers=NUM_DRIVERS,
            num_establishments=NUM_ESTABLISHMENTS,
            num_orders=NUM_ORDERS,
            num_costumers=NUM_COSTUMERS,
            grid_map_size=GRID_MAP_SIZE,
            vel_drivers=VEL_DRIVERS,
            prepare_time=PREPARE_TIME,
            operating_radius=OPERATING_RADIUS,
            production_capacity=PRODUCTION_CAPACITY,
            percentage_allocation_driver=PERCENTAGE_ALLOCATION_DRIVER,
            use_estimate=True,
            desconsider_capacity=True,
            max_time_step=MAX_TIME_STEP,
            reward_objective=REWARD_OBJECTIVE,
            function=FUNCTION,
            lambda_code=LAMBDA_CODE,
            time_shift=TIME_SHIFT,
            normalize=NORMALIZE,
        )])

        # Criando o EvalCallback para salvar o melhor modelo
        eval_callback = EvalCallback(
            eval_env,
            best_model_save_path=DIR_PATH + "best_model/",
            log_path=DIR_PATH + "logs/",
            eval_freq=5000,  # Avaliação a cada 5k timesteps
            deterministic=True,
            render=False
        )

        # Treinar o modelo com EvalCallback
        model = PPO('MultiInputPolicy', env, verbose=1, tensorboard_log=DIR_PATH + "ppo_tensorboard/")
        start_time = time.time()
        model.learn(total_timesteps=6000000, callback=eval_callback)
        end_time = time.time()
        training_time = end_time - start_time

        # Converter segundos para hh:MM:ss
        hours = int(training_time // 3600)
        minutes = int((training_time % 3600) // 60)
        seconds = int(training_time % 60)
        formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"

        print(f"Total Training Time: {formatted_time}")

        with open(DIR_PATH + "training_time.txt", "w", encoding="utf-8") as time_training_file:
            time_training_file.write(f"Tempo total de treinamento: {formatted_time}\n")

        # Salvar o modelo final
        model.save(DIR_PATH + "final_model")

        # Carregar os dados do Monitor para análise
        log_data = pd.read_csv(DIR_PATH + "logs/monitor.csv", skiprows=1)

        # Plotar recompensa acumulada por episódio
        retornos = log_data["r"].values 
        plt.figure(figsize=(10, 5))
        plt.plot(retornos, label="Recompensa")
        plt.xlabel("Episódios")
        plt.ylabel("Recompensa")
        plt.title("Curva de Aprendizado - Recompensa por Episódio")
        plt.legend()
        plt.savefig(DIR_PATH + "curva_de_aprendizado.png", dpi=300, bbox_inches='tight')
        plt.show()

        # Calcular a média e o desvio padrão a cada mil episódios
        media_1000_episodios = []
        desvio_1000_episodios = []
        for i in range(1000, len(retornos), 1000):
            media_1000_episodios.append(np.mean(retornos[i-1000:i]))
            desvio_1000_episodios.append(np.std(retornos[i-1000:i]))
        media_1000_episodios = np.array(media_1000_episodios)
        desvio_1000_episodios = np.array(desvio_1000_episodios)

        # Plotar a curva de aprendizado com a média e o desvio padrão
        plt.figure(figsize=(10, 5))
        plt.plot(media_1000_episodios, label="Média a cada 1000 episódios")
        plt.fill_between(range(len(media_1000_episodios)), media_1000_episodios - desvio_1000_episodios, media_1000_episodios + desvio_1000_episodios, alpha=0.2, label="Desvio Padrão")
        plt.title('Curva de Aprendizado (média e desvio padrão a cada mil episódios)')
        plt.xlabel('Episódios (x1000)')
        plt.ylabel('Retornos')
        plt.legend()
        plt.savefig(DIR_PATH + "curva_de_aprendizado_avg_std_1000_ep.png", dpi=300, bbox_inches='tight')
        plt.show()

    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()

if SAVE_LOG_TO_FILE:
    log_file.close()
