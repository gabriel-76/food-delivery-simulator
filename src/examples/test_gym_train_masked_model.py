from stable_baselines3 import PPO
from stable_baselines3.common.env_checker import check_env
from stable_baselines3.common.vec_env import DummyVecEnv
import gymnasium as gym
import numpy as np
from sb3_contrib.common.wrappers import ActionMasker
from sb3_contrib import MaskablePPO

from src.main.environment.food_delivery_gym_masked_matrix_env import FoodDeliveryGymMatrixEnv
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

# Função de máscara de ação
def mask_fn(env: gym.Env) -> np.ndarray:
    return env.valid_action_mask()

def main():
    environment = FoodDeliverySimpyEnv(
        map=GridMap(100),
        generators=[
            InitialCustomerGenerator(NUM_ORDERS),
            InitialEstablishmentGenerator(10),
            InitialDriverGenerator(NUM_DRIVERS),
            InitialOrderGenerator(NUM_ORDERS)
        ],
        optimizer=None,
        view=GridViewPygame()
    )

    gym_env = FoodDeliveryGymMatrixEnv(environment, num_drivers=NUM_DRIVERS, num_orders=NUM_ORDERS)

    gym_env = ActionMasker(gym_env, mask_fn)

    # Verificar se o ambiente está implementado corretamente
    check_env(gym_env, warn=True)

    # Vectorize environment
    env = DummyVecEnv([lambda: gym_env])

    # Treinar o modelo
    model = MaskablePPO('MultiInputPolicy', env, verbose=1)
    model.learn(total_timesteps=10000)

    # Salvar o modelo
    model.save("ppo_delivery")

    # Carregar o modelo
    model = MaskablePPO.load("ppo_delivery")

    environment = FoodDeliverySimpyEnv(
        map=GridMap(100),
        generators=[
            InitialCustomerGenerator(NUM_ORDERS),
            InitialEstablishmentGenerator(20),
            InitialDriverGenerator(NUM_DRIVERS),
            InitialOrderGenerator(NUM_ORDERS)
        ],
        optimizer=None,
        view=GridViewPygame()
    )

    gym_env = FoodDeliveryGymMatrixEnv(environment, num_drivers=NUM_DRIVERS, num_orders=NUM_ORDERS, render_mode='human')
    gym_env = ActionMasker(gym_env, mask_fn)

    # Testar o modelo treinado
    obs, info = gym_env.reset()
    for _ in range(1000):
        action_masks = mask_fn(gym_env)  # Obtém as máscaras de ações válidas
        action, _states = model.predict(obs, action_masks=action_masks)
        obs, rewards, dones, truncated, info = gym_env.step(action)
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

if __name__ == '__main__':
    main()
