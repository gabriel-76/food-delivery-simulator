from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv

from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv

NUM_DRIVERS = 5
NUM_ORDERS = 200
NUM_ESTABLISHMENTS = 5
NUM_COSTUMERS = NUM_ORDERS

def main():
    try:
        gym_env = FoodDeliveryGymEnv(
            num_drivers=NUM_DRIVERS, 
            num_establishments=NUM_ESTABLISHMENTS, 
            num_orders=NUM_ORDERS, 
            num_costumers=NUM_COSTUMERS, 
            seed=2345,
            use_estimate=True, 
            desconsider_capacity=True, 
            max_time_step=10000, 
            reward_objective=1,
            render_mode='human'
        )

        # Verificar se o ambiente está implementado corretamente
        # check_env(gym_env, warn=True)

        estado : list[int] = gym_env.reset()
        print(f'estado inicial {estado}')

        # done : bool = False
        for i in range(10):
            # acao = 1
            acao = gym_env.action_space.sample() # Ação aleatória
            print("------------------> Step " + str(i+1) +" <------------------")
            print(f'{acao=}')
            print(f'estado_antes={estado}')
            options = {
                "customers": False,
                "establishments": True,
                "drivers": True,
                "orders": False,
                "events": False,
                "orders_delivered": True
            }
            gym_env.print_enviroment_state(options)
            estado, recompensa, done, truncado, info = gym_env.step(acao)
            print(f'estado_depois={estado}')
            print(f'{recompensa=}')

            if done:
                print("Done!")
                break

        # gym_env.show_statistcs_board()

    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()
