import sys
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv

from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv

NUM_DRIVERS = 10
NUM_ORDERS = 12*24 # 12 pedidos por hora durante 24 horas
NUM_ESTABLISHMENTS = 10
NUM_COSTUMERS = NUM_ORDERS
GRID_MAP_SIZE = 50 # Tamanho do grid 50x50
MAX_TIME_STEP = 60*24*2 # 2 dias
# 2 pedidos de 10 em 10 minutos
FUNCTION = lambda time: 2
TIME_SHIFT = 10

# Variáveis para criação dos Motoristas
VEL_DRIVERS = [3, 5]

# Variáveis para criação dos Estabelecimentos
PREPARE_TIME = [20, 60]
OPERATING_RADIUS = [5, 30]
PRODUCTION_CAPACITY = [1, 4]

# Variável que controla quando o motorista deve ser alocado
# A porcentagem se refere ao progresso de preparação do pedido
# Exemplo: 0.7 indica que o motorista deve será alocado quando o pedido estiver 70% pronto
PERCENTAGE_ALLOCATION_DRIVER = 0.7

SEED = 101010

# Escolha se deseja salvar o log em um arquivo
SAVE_LOG_TO_FILE = True

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
            seed=SEED,
            use_estimate=True, 
            desconsider_capacity=True, 
            max_time_step=MAX_TIME_STEP, 
            reward_objective=1,
            function=FUNCTION,
            time_shift=TIME_SHIFT,
            #render_mode='human'
        )

        # Verificar se o ambiente está implementado corretamente
        # check_env(gym_env, warn=True)

        estado : list[int] = gym_env.reset()
        print(f'estado inicial {estado}')

        i = 1
        done = False
        soma_recompensa = 0
        np.random.seed(SEED)
        while not done:
            # acao = 1
            # acao = gym_env.action_space.sample() # Ação aleatória
            acao = np.random.randint(0, 10) # Ação aleatória segundo a seed
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