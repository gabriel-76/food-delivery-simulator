import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv

from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv

NUM_DRIVERS = 10
NUM_ORDERS = 20
NUM_ESTABLISHMENTS = 10
NUM_COSTUMERS = NUM_ORDERS
MAX_TIME_STEP = 100000
SEED = 101010

def main():
    try:
        gym_env = FoodDeliveryGymEnv(
            num_drivers=NUM_DRIVERS, 
            num_establishments=NUM_ESTABLISHMENTS, 
            num_orders=NUM_ORDERS, 
            num_costumers=NUM_COSTUMERS, 
            seed=SEED,
            use_estimate=True, 
            desconsider_capacity=True, 
            max_time_step=MAX_TIME_STEP, 
            reward_objective=1,
            # render_mode='human'
        )

        # Verificar se o ambiente está implementado corretamente
        # check_env(gym_env, warn=True)

        # TODO - Motorista saiu pra buscar o pedido antes de ele entrar em preparação
        # TODO - Adicionar tempo em que o motorista levaria para entregar o novo ao novo cliente no observation space
        # TODO - Adicionar um atributo ao driver para guardar o último lugar que ele estaria e atualizá-lo

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
            gym_env.print_enviroment_state()
            print(f'estado_depois={estado}')
            print(f'{recompensa=}')
            soma_recompensa += recompensa
            i += 1
        
        print("--------------> Fim do ambiente <--------------")
        gym_env.print_enviroment_state()
        print(f'observação final = {gym_env.get_observation()}')
        print(f'soma das recompensas = {soma_recompensa}')
        print(f'quantidade de rotas criadas = {gym_env.simpy_env.state.get_length_orders()}')
        print(f'quantidade de rotas entregues = {gym_env.simpy_env.state.orders_delivered}')

        # gym_env.show_statistcs_board()

    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()
