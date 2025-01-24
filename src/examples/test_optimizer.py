from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv
from src.main.optimizer.optimizer_gym.random_driver_optimizer_gym import RandomDriverOptimizerGym

NUM_DRIVERS = 10
NUM_ORDERS = 12*24 # 12 pedidos por hora durante 24 horas
NUM_ESTABLISHMENTS = 10
NUM_COSTUMERS = NUM_ORDERS
GRID_MAP_SIZE = 50 # Tamanho do grid 50x50
REWARD_OBJECTIVE = 1
MAX_TIME_STEP = 60*24*2 # 2 dias
# 2 pedidos de 10 em 10 minutos
FUNCTION = lambda time: 2
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

NORMALIZE = False
SEED = 101010


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
        time_shift=TIME_SHIFT,
        normalize=NORMALIZE,
        #render_mode='human'
    )

    optimizer = RandomDriverOptimizerGym(gym_env, seed=SEED)

    optimizer.run()

if __name__ == '__main__':
    main()