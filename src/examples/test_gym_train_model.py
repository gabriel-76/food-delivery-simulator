from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv

from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv

NUM_DRIVERS = 1
NUM_ORDERS = 5
NUM_ESTABLISHMENTS = 10
NUM_COSTUMERS = NUM_ORDERS

def main():
    try:
        gym_env = FoodDeliveryGymEnv(
            num_drivers=NUM_DRIVERS, 
            num_establishments=NUM_ESTABLISHMENTS, 
            num_orders=NUM_ORDERS, 
            num_costumers=NUM_COSTUMERS, 
            seed=10,
            use_estimate=True, 
            desconsider_capacity=True, 
            max_time_step=10000, 
            reward_objective=1
        )

        # Verificar se o ambiente está implementado corretamente
        check_env(gym_env, warn=True)

        # Vectorize environment
        env = DummyVecEnv([lambda: gym_env])

        # Treinar o modelo
        model = PPO('MultiInputPolicy', env, verbose=1)
        model.learn(total_timesteps=10000)

        # Salvar o modelo
        model.save("ppo_delivery")

        # Carregar o modelo
        model = PPO.load("ppo_delivery")

        # Testar o modelo treinado
        obs, info = gym_env.reset(options={"render_mode": "human"})
        for _ in range(1000):
            action, _states = model.predict(obs)
            obs, reward, done, truncated, info = gym_env.step(action)
            # print(obs, rewards, dones, info)
            gym_env.render()

        gym_env.show_statistcs_board()

    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()
