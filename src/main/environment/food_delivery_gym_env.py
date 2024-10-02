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

    def __init__(self, simpy_env: FoodDeliverySimpyEnv, num_drivers, num_establishments, num_orders, max_time_step=10000, reward_objective=1, render_mode=None):
        self.num_drivers = num_drivers
        self.num_establishments = num_establishments
        self.num_orders = num_orders
        self.simpy_env = simpy_env

        self.last_order = None
        self.last_num_orders_delivered = 0

        # Definindo o objetivo da recompensa
        valid_objectives = [1, 2]
        if reward_objective not in valid_objectives:
            raise ValueError(f"Objetivo inválido! Escolha entre {valid_objectives}")
        self.reward_objective = reward_objective

        # Espaço de Observação
        self.observation_space = Dict({
            'drivers_busy_time': Box(low=0, high=np.inf, shape=(self.num_drivers, 1), dtype=np.int32),
            'pending_orders': Discrete(self.num_orders + 1),
            'establishment_busy_time': Box(low=0, high=np.inf, shape=(self.num_establishments, 1), dtype=np.int32),
            'current_time_step': Discrete(max_time_step) #TODO: Perguntar como definir o limite de tempo de forma correta
        })

        # Espaço de Ação
        self.action_space = Discrete(self.num_drivers)  # Escolher qual driver pegará o pedido

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

    def get_observation(self):
        # 1. drivers_busy_time: Tempo de ocupação de cada motorista
        drivers_busy_time = np.zeros((self.num_drivers, 1), dtype=np.int32)
        for i, driver in enumerate(self.simpy_env.state.drivers):
            drivers_busy_time[i] = driver.estimate_total_busy_time()

        # 2. pending_orders: Número de pedidos pendentes
        pending_orders = len([order for order in self.simpy_env.state.orders if order.status == OrderStatus.READY])

        # 3. establishment_next_order_ready_time: Tempo que falta para o próximo pedido em preparação de cada restaurante ficar pronto
        establishment_busy_time = np.zeros((self.num_establishments, 1), dtype=np.int32)
        for i, establishment in enumerate(self.simpy_env.state.establishments):
            establishment_busy_time[i] = establishment.get_establishment_busy_time()

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
    
    def _get_obs(self):
        return self.get_observation()

    def reset(self, seed=None, options=None):
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        self.simpy_env = FoodDeliverySimpyEnv(
            map=self.simpy_env.map,
            generators=self.simpy_env.generators,
            optimizer=self.simpy_env.optimizer,
            view=self.simpy_env.view
        )

        # TODO: Separar em uma função -> Evitar replicação de código
        core_event = None
        while core_event is None:
            if (self.simpy_env.state.orders_delivered < self.num_orders):
                # print('self.simpy_env.peek(): ' + str(self.simpy_env.peek()))
                self.simpy_env.step()
                core_event = self.simpy_env.dequeue_core_event()

        self.last_order = core_event.order

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
            time_to_complete_order = last_driver_selected.estimate_total_busy_time()
        
        # Distância total percorrida pelos drivers #TODO: Será que uma recompensa negativa que sempre aumenta está certo?
        sum_distance_drivers = 0
        for driver in self.simpy_env.state.drivers:
            sum_distance_drivers += driver.total_distance

        # Objetivo 1: Minimizar o tempo de entrega -> Recompensa negativa
        if self.reward_objective == 1:
            reward_time = -time_to_complete_order
            return reward_time
        # Objetivo 2: Minimizar o custo de operação (distância) -> Recompensa negativa
        elif self.reward_objective == 2:
            reward_distance = -sum_distance_drivers
            return reward_distance
        
    def step(self, action):
        if self.render_mode == "human":
            truncated = self.simpy_env.view.quited

        terminated = False
        print("------------------> Step <------------------")
        print("action: {}".format(action))
        print("last_order: {}".format(vars(self.last_order)))
        selected_driver = self.simpy_env.state.drivers[action]
        self.select_driver_to_order(selected_driver, self.last_order)

        # TODO: Separar em uma função -> Evitar replicação de código
        core_event = None
        while (not terminated) and (core_event is None):
            if (self.simpy_env.state.orders_delivered < self.num_orders):
                # print('self.simpy_env.peek(): ' + str(self.simpy_env.peek()))
                self.simpy_env.step()

                if (self.simpy_env.state.orders_delivered > self.last_num_orders_delivered):
                    print("Pedido entregue!")
                    print("Número de pedidos entregues: {}".format(self.simpy_env.state.orders_delivered))
                    self.last_num_orders_delivered = self.simpy_env.state.orders_delivered

                core_event = self.simpy_env.dequeue_core_event()
            else:
                terminated = True

        self.last_order = core_event.order
        
        truncated = False
        reward = self.calculate_reward(selected_driver)
        print("reward: {}".format(reward))
        observation = self._get_obs()
        assert self.observation_space.contains(observation), "A observação gerada não está contida no espaço de observação."
        info = self._get_info()

        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "human":
            self.simpy_env.render()

    def close(self):
        self.simpy_env.close()
