import sys
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

if SAVE_LOG_TO_FILE:
    log_file = open("log.txt", "w", encoding="utf-8")
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
            time_shift=TIME_SHIFT,
            normalize=NORMALIZE,
        )

        # Verificar se o ambiente está implementado corretamente
        check_env(gym_env, warn=True)

        # Monitorando o ambiente de treinamento
        gym_env = Monitor(gym_env, "logs/")
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
            time_shift=TIME_SHIFT,
            normalize=NORMALIZE,
        )])

        # Criando o EvalCallback para salvar o melhor modelo
        eval_callback = EvalCallback(
            eval_env,
            best_model_save_path="./best_model/",
            log_path="./logs/",
            eval_freq=5000,  # Avaliação a cada 5k timesteps
            deterministic=True,
            render=False
        )

        # Treinar o modelo com EvalCallback
        model = PPO('MultiInputPolicy', env, verbose=1, tensorboard_log="./ppo_tensorboard/")
        model.learn(total_timesteps=1000000, callback=eval_callback)

        # Salvar o modelo final
        model.save("ppo_delivery")

        # Carregar os dados do Monitor para análise
        log_data = pd.read_csv("logs/monitor.csv", skiprows=1)

        # Plotar recompensa média acumulada por episódio
        plt.figure(figsize=(10, 5))
        plt.plot(log_data["r"].rolling(window=10).mean(), label="Recompensa Média (rolling 10)")
        plt.xlabel("Episódios")
        plt.ylabel("Recompensa")
        plt.title("Curva de Aprendizado - Recompensa por Episódio")
        plt.legend()
        plt.show()

        # Carregar o melhor modelo treinado
        model = PPO.load("./best_model/best_model.zip")

        # Testar o modelo treinado
        obs, info = gym_env.reset(options={'render_mode': 'human'})

        i = 1
        done = False
        truncated = False

        while (not done) and (not truncated) and (i <= 1000):
            action, _states = model.predict(obs)
            obs, reward, done, truncated, info = gym_env.step(action)
            i += 1

        gym_env.env.show_statistcs_board()

    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()

if SAVE_LOG_TO_FILE:
    log_file.close()
