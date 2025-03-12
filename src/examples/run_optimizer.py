import sys

from stable_baselines3 import PPO
from src.main.cost.objective_based_cost_function import ObjectiveBasedCostFunction
from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv
from src.main.optimizer.optimizer_gym.first_driver_optimizer_gym import FirstDriverOptimizerGym
from src.main.optimizer.optimizer_gym.lowest_cost_driver_optimizer_gym import LowestCostDriverOptimizerGym
from src.main.optimizer.optimizer_gym.nearest_driver_optimizer_gym import NearestDriverOptimizerGym
from src.main.optimizer.optimizer_gym.random_driver_optimizer_gym import RandomDriverOptimizerGym
from src.main.optimizer.optimizer_gym.rl_model_optimizer_gym import RLModelOptimizerGym

NUM_DRIVERS = 10
NUM_ORDERS = 12*24 # 12 pedidos por hora durante 24 horas
NUM_ESTABLISHMENTS = 10
NUM_COSTUMERS = NUM_ORDERS
GRID_MAP_SIZE = 50 # Tamanho do grid 50x50
REWARD_OBJECTIVE = 1
MAX_TIME_STEP = 60*24*2 # 2 dias
# 2 pedidos de 10 em 10 minutos
FUNCTION = lambda time: 2
LAMBDA_CODE = "lambda time: 2"
TIME_SHIFT = 10

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

RESULTS_DIR = "./data/200_runs_with_all_agents/"

if SAVE_LOG_TO_FILE:
    log_file = open(RESULTS_DIR + "log.txt", "w", encoding="utf-8")
    sys.stdout = log_file
    sys.stderr = log_file

def main():
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
        #render_mode='human'
    )

    num_runs = 20

    optimizer = RandomDriverOptimizerGym(gym_env)
    optimizer.run_simulations(num_runs, RESULTS_DIR + "random_heuristic/", seed=SEED)

    optimizer = FirstDriverOptimizerGym(gym_env)
    optimizer.run_simulations(num_runs, RESULTS_DIR + "first_driver_heuristic/", seed=SEED)

    optimizer = NearestDriverOptimizerGym(gym_env)
    optimizer.run_simulations(num_runs, RESULTS_DIR + "nearest_driver_heuristic/", seed=SEED)

    optimizer = LowestCostDriverOptimizerGym(gym_env, cost_function=ObjectiveBasedCostFunction(objective=REWARD_OBJECTIVE))
    optimizer.run_simulations(num_runs, RESULTS_DIR + "lowest_cost_driver_heuristic/", seed=SEED)

    optimizer = RLModelOptimizerGym(gym_env, PPO.load("./data/ppo_training/13000000 eps/best_model/best_model.zip"))
    optimizer.run_simulations(num_runs, RESULTS_DIR + "ppo_agent_trained_13000000/", seed=SEED)


if __name__ == '__main__':
    main()

if SAVE_LOG_TO_FILE:
    log_file.close()