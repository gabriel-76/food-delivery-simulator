import sys
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env

from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv

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

NORMALIZE = True
SEEDS = [96201, 497000, 720394, 975084, 774393, 759633, 454796, 204492, 62982, 636872,
 90356, 857421, 255340, 551433, 928406, 919090, 731526, 367840, 826456, 376960,
 847025, 536052, 916556, 459777, 146860, 335491, 52134, 965297, 915470, 818817,
 382679, 427253, 390943, 529428, 312234, 82662, 353958, 716083, 409375, 210292,
 643406, 601819, 705268, 674149, 953364, 930811, 612797, 42270, 298820, 589932,
 286904, 426789, 206074, 976086, 82148, 136708, 806702, 740858, 894270, 228764,
 282714, 622764, 766666, 940901, 119402, 536, 336219, 537844, 215331, 16873,
 805198, 237897, 448121, 352713, 574553, 900860, 823072, 70946, 293568, 261891,
 290672, 669883, 562722, 319212, 786031, 380548, 381022, 416983, 416964, 814920,
 184754, 266952, 685201, 782267, 648630, 712872, 163457, 547493, 249258, 800258,
 670432, 385484, 808916, 227062, 836645, 74436, 243047, 690344, 738879, 104162,
 600690, 788223, 122610, 508020, 846147, 517509, 522001, 325753, 67211, 502914,
 801431, 111305, 509008, 15661, 469966, 230849, 281482, 43646, 341766, 937782,
 933963, 755295, 82074, 574613, 111948, 651258, 352833, 389444, 988596, 246629,
 327239, 426148, 815528, 70006, 206969, 839230, 605280, 405068, 566326, 276890,
 688297, 558110, 168574, 822504, 546932, 824092, 364871, 782401, 358037, 212148,
 789893, 750291, 352712, 682352, 190424, 575842, 856409, 375330, 805131, 224508,
 286116, 930337, 991659, 305142, 477310, 96329, 765496, 925841, 357591, 730413,
 207385, 113670, 59683, 85663, 209367, 17341, 742336, 606249, 745645, 320185,
 57514, 808264, 133167, 245265, 118631, 752217, 764925, 379876, 91719, 294812]

# Escolha se deseja salvar o log em um arquivo
SAVE_LOG_TO_FILE = False

RESULTS_FILE = "C:/Users/marco/OneDrive/Área de Trabalho/Modelo treinado 6000000 PPO/results.txt"

if SAVE_LOG_TO_FILE:
    log_file = open("log.txt", "w", encoding="utf-8")
    sys.stdout = log_file
    sys.stderr = log_file

def main():
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

    check_env(gym_env, warn=True)

    # Carregar o melhor modelo treinado
    model = PPO.load("./best_model.zip")

    total_rewards = []
    num_runs = 200

    with open(RESULTS_FILE, "w", encoding="utf-8") as results_file:
        for i in range(num_runs):
            seed = SEEDS[i]
            print(f"Run {i + 1} - Seed: {seed}")

            # Testar o modelo treinado
            obs, info = gym_env.reset(seed=seed)

            sum_reward = 0
            done = False
            truncated = False
            while (not done) and (not truncated) and (i <= 1000):
                action, _states = model.predict(obs)
                obs, reward, done, truncated, info = gym_env.step(action)
                sum_reward += reward

            gym_env.show_statistcs_board()

            total_rewards.append(sum_reward)

            results_file.write(f"Execução {i + 1}: Seed = {seed}, Soma das Recompensas = {sum_reward}\n")

        avg_reward = sum(total_rewards) / num_runs
        results_file.write(f"\nMédia das somas das recompensas: {avg_reward:.2f}\n")
    
    print(f"Resultados salvos em {RESULTS_FILE}")


if __name__ == '__main__':
    main()

if SAVE_LOG_TO_FILE:
    log_file.close()