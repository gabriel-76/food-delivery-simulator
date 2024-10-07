from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv

from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_customer_generator import InitialCustomerGenerator
from src.main.generator.initial_driver_generator import InitialDriverGenerator
from src.main.generator.initial_order_generator import InitialOrderGenerator
from src.main.generator.initial_establishment_generator import InitialEstablishmentGenerator
from src.main.map.grid_map import GridMap
from src.main.statistic.custom_board import CustomBoard
from src.main.statistic.delay_metric import DelayMetric
from src.main.statistic.distance_metric import DistanceMetric
from src.main.statistic.driver_status_metric import DriverStatusMetric
from src.main.statistic.order_curve_metric import OrderCurveMetric
from src.main.statistic.order_status_metric import OrderStatusMetric
from src.main.statistic.total_metric import TotalMetric
from src.main.view.grid_view_pygame import GridViewPygame

NUM_DRIVERS = 1
NUM_ORDERS = 5
NUM_ESTABLISHMENTS = 10
NUM_COSTUMERS = NUM_ORDERS

def main():
    try:
        gym_env = FoodDeliveryGymEnv(num_drivers=NUM_DRIVERS, num_establishments=NUM_ESTABLISHMENTS, num_orders=NUM_ORDERS, num_costumers=NUM_COSTUMERS, use_estimate=True, desconsider_capacity=True, max_time_step=10000, reward_objective=1)

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

        custom_board = CustomBoard(metrics=[
            OrderCurveMetric(gym_env.simpy_env),
            TotalMetric(gym_env.simpy_env),
            DistanceMetric(gym_env.simpy_env),
            DelayMetric(gym_env.simpy_env),
            DriverStatusMetric(gym_env.simpy_env),
            OrderStatusMetric(gym_env.simpy_env),
        ])
        custom_board.view()

    except ValueError as e:
        print(e)


if __name__ == '__main__':
    main()
