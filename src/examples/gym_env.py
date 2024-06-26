from src.main.environment.food_delivery_gym_env import FoodDeliveryGymEnv
from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_customer_generator import InitialCustomerGenerator
from src.main.generator.initial_driver_generator import InitialDriverGenerator
from src.main.generator.initial_establishment_generator import InitialEstablishmentGenerator
from src.main.generator.initial_order_generator import InitialOrderGenerator
from src.main.map.grid_map import GridMap
from src.main.optimizer.random_driver_optimizer import RandomDriverOptimizer
from src.main.view.grid_view_pygame import GridViewPygame


def main():
    environment = FoodDeliverySimpyEnv(
        map=GridMap(100),
        generators=[
            InitialCustomerGenerator(100),
            InitialEstablishmentGenerator(100, use_estimate=True),
            InitialDriverGenerator(100),
            InitialOrderGenerator(1000)
        ],
        optimizer=RandomDriverOptimizer(),
        # view=GridViewMatplotlib()
        view=GridViewPygame()
    )

    gym_env = FoodDeliveryGymEnv(environment, render_mode='human')

    done = False
    quit = False
    counter = 1

    while not done and not quit and counter < 300:
        action = gym_env.action_space.sample()  # Selecionar uma ação aleatória
        # obs, reward, done, truncated, info = gym_env.step(action) # Executar passo a passo
        obs, reward, done, quit, info = gym_env.run(action)  # Executar em unidades de tempo
        print(f'Observation: {obs}, Reward: {reward}, Done: {done}, Info: {info}')
        gym_env.render()
        counter += 1


if __name__ == '__main__':
    main()
