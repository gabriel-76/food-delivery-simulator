import sys
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv

from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv

NUM_DRIVERS = 10
NUM_ORDERS = 45*24 # 45 pedidos por hora durante 24 horas
NUM_ESTABLISHMENTS = 10
NUM_COSTUMERS = NUM_ORDERS
GRID_MAP_SIZE = 50 # Tamanho do grid 50x50
REWARD_OBJECTIVE = 1
MAX_TIME_STEP = 60*24*2 # 2 dias
# 2 pedidos de 10 em 10 minutos
FUNCTION = lambda time: 3
LAMBDA_CODE = "lambda time: 3"
TIME_SHIFT = 4

# Variáveis para criação dos Motoristas
VEL_DRIVERS = [3, 5]

# Variáveis para criação dos Estabelecimentos
PREPARE_TIME = [20, 60]
OPERATING_RADIUS = [5, 30]
PRODUCTION_CAPACITY = [4, 4]

# Variável que controla quando o motorista deve ser alocado
# A porcentagem se refere ao progresso de preparação do pedido
# Exemplo: 0.7 indica que o motorista deve será alocado quando o pedido estiver 70% pronto
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
            render_mode='human'
        )

        # Verificar se o ambiente está implementado corretamente
        # check_env(gym_env, warn=True) 

        estado : list[int] = gym_env.reset(seed=SEED)
        print(f'estado inicial {estado}')

        i = 1
        done = False
        truncado = False
        soma_recompensa = 0
        while not done and not truncado:
            acao = gym_env.action_space.sample() # Ação aleatória
            print("------------------> Step " + str(i) +" <------------------")
            print(f'{acao=}')
            estado, recompensa, done, truncado, info = gym_env.step(acao)
            gym_env.simpy_env.print_enviroment_state()
            print(f'estado_depois={estado}')
            print(f'{recompensa=}')
            soma_recompensa += recompensa
            i += 1
        
        print("--------------> Fim do ambiente <--------------")
        gym_env.simpy_env.print_enviroment_state()
        print(f'observação final = {gym_env.get_observation()}')
        print(f'soma das recompensas = {soma_recompensa}')
        print(f'quantidade de rotas criadas = {gym_env.simpy_env.state.get_length_orders()}')
        print(f'quantidade de rotas entregues = {gym_env.simpy_env.state.orders_delivered}')

        gym_env.show_statistcs_board()

    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()

if SAVE_LOG_TO_FILE:
    log_file.close()