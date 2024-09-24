import numpy as np
from gymnasium import Env
from gymnasium.spaces import Dict, Sequence, Box, Discrete, Tuple, MultiDiscrete

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.order.order_status import OrderStatus
from src.main.route.delivery_route_segment import DeliveryRouteSegment
from src.main.route.pickup_route_segment import PickupRouteSegment
from src.main.route.route import Route


class FoodDeliveryGymEnv(Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, simpy_env: FoodDeliverySimpyEnv, num_drivers, num_establishments, num_orders, render_mode=None):
        self.num_drivers = num_drivers
        self.num_establishments = num_establishments
        self.num_orders = num_orders
        self.simpy_env = simpy_env

        self.last_order = None
        self.last_driver_selected = None

        # Espaço de Observação
        self.observation_space = Dict({
            'drivers_busy_time': Box(low=0, high=np.inf, shape=(self.num_drivers, 1), dtype=np.int32),
            'pending_orders': Discrete(self.num_orders + 1),
            'establishment_busy_time': Box(low=0, high=np.inf, shape=(self.num_establishments, 1), dtype=np.int32),
            'current_time_step': Discrete(1000)
        })

        # Espaço de Ação
        self.action_space = Discrete(self.num_drivers)  # Escolher qual driver pegará o pedido

        # Inicializando variáveis internas
        self.drivers = np.zeros((self.num_drivers, 1))  # Tempo para coletar o pedido
        self.pending_orders = 0  # Número de pedidos pendentes
        self.restaurant_wait_time = np.zeros(self.num_restaurants, 1)  # Tempo até o próximo pedido
        self.current_time_step = self.simpy_env.now  # Tempo atual

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def get_observation(self):
        # 1. drivers_busy_time: Tempo de ocupação de cada motorista
        drivers_busy_time = np.zeros((self.num_drivers, 1), dtype=np.int32)
        for i, driver in enumerate(self.simpy_env.state.drivers):
            drivers_busy_time[i] = driver.estimate_total_busy_time()

        # 2. pending_orders: Número de pedidos pendentes
        pending_orders = len([order for order in self.simpy_env.state.orders if order.status == OrderStatus.READY])

        # 3. establishment_busy_time: Tempo que falta para o último pedido em preparação de cada restaurante
        establishment_busy_time = np.zeros((self.num_establishments, 1), dtype=np.int32)
        for i, establishment in enumerate(self.simpy_env.state.establishments):
            establishment_busy_time[i] = establishment.overloaded_until

        # 4. current_time_step: O tempo atual da simulação (número do passo)
        current_time_step = self.simpy_env.now

        # Criando a observação final no formato esperado
        obs = {
            'drivers_busy_time': drivers_busy_time,
            'pending_orders': pending_orders,
            'establishment_busy_time': establishment_busy_time,
            'current_time_step': current_time_step
        }

        return obs
       
    def _get_info(self):
        return {'info': self.simpy_env.now}

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self.simpy_env = FoodDeliverySimpyEnv(
            map=self.simpy_env.map,
            generators=self.simpy_env.generators,
            optimizer=self.simpy_env.optimizer,
            view=self.simpy_env.view
        )

        observation = self._get_obs()
        info = self._get_info()

        self.render()

        return observation, info
    
    def select_driver_to_order(self, selected_driver, order):
        segment_pickup = PickupRouteSegment(order)
        segment_delivery = DeliveryRouteSegment(order)
        route = Route(self.simpy_env, [segment_pickup, segment_delivery])
        selected_driver.receive_route_requests(route)

    def calculate_reward(self, last_driver_selected):
        # Tempo total gasto para o driver entregar o último pedido
        # Se o driver for nulo ou pedido não foi entregue, o tempo é 0
        time_to_complete_order = 0
        if last_driver_selected is not None:
            time_to_complete_order = last_driver_selected.get_and_clear_time_spent_to_last_order()
        
        # Distância total percorrida pelos drivers
        sum_distance_drivers = 0
        for driver in self.simpy_env.state.drivers:
            sum_distance_drivers += driver.total_distance
            driver.get_and_clear_time_spent_to_last_order()
        
        # Objetivo 1: Minimizar o tempo de entrega -> Recompensa negativa
        reward_time = -time_to_complete_order
        
        # Objetivo 2: Minimizar o custo de operação (distância) -> Recompensa negativa
        reward_distance = -sum_distance_drivers
        
        return reward_time + reward_distance
        
    def step(self, action):
        if self.render_mode == "human":
            truncated = self.simpy_env.view.quited

        core_event = None
        while (self.simpy_env.peek() < self.simpy_env.now + 1) or core_event is not None:
            print(self.simpy_env.peek())
            # simpy_env.step(render_mode='human')
            self.simpy_env.step()
            core_event = self.simpy_env.dequeue_core_event()
        
        # Verificar se o episódio terminou
        terminated = False
        truncated = False
        observation = self._get_obs()
        assert self.observation_space.contains(observation), "A observação gerada não está contida no espaço de observação."
        info = self._get_info()

        print('Next client ready order event')
        print(action)
        print(core_event.order)
        selected_driver = self.drivers[action]
        self.apply_action(selected_driver, core_event.order)

        reward = self.calculate_reward(last_driver_selected) # type: ignore

        self.last_order = core_event.order
        self.last_driver_selected = selected_driver

        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "human":
            self.simpy_env.render()

    def close(self):
        self.simpy_env.close()
