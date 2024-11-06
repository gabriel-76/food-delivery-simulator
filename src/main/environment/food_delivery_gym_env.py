import numpy as np
from gymnasium import Env
from gymnasium.spaces import Dict, Sequence, Box, Discrete, Tuple, MultiDiscrete

from src.main.environment.food_delivery_simpy_env import FoodDeliverySimpyEnv
from src.main.generator.initial_customer_generator import InitialCustomerGenerator
from src.main.generator.initial_driver_generator import InitialDriverGenerator
from src.main.generator.initial_establishment_generator import InitialEstablishmentGenerator
from src.main.generator.initial_establishment_order_rate_generator import InitialEstablishmentOrderRateGenerator
from src.main.generator.initial_order_generator import InitialOrderGenerator
from src.main.generator.time_shift_order_establishment_rate_generator import TimeShiftOrderEstablishmentRateGenerator
from src.main.map.grid_map import GridMap
from src.main.order.order_status import OrderStatus
from src.main.route.delivery_route_segment import DeliveryRouteSegment
from src.main.route.pickup_route_segment import PickupRouteSegment
from src.main.route.route import Route
from src.main.statistic.custom_board import CustomBoard
from src.main.statistic.delay_metric import DelayMetric
from src.main.statistic.distance_metric import DistanceMetric
from src.main.statistic.driver_status_metric import DriverStatusMetric
from src.main.statistic.order_curve_metric import OrderCurveMetric
from src.main.statistic.order_status_metric import OrderStatusMetric
from src.main.statistic.total_metric import TotalMetric
from src.main.view.grid_view_pygame import GridViewPygame


class FoodDeliveryGymEnv(Env):
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 4}

    def __init__(self, num_drivers, num_establishments, num_orders, num_costumers, grid_map_size=100, use_estimate=True, desconsider_capacity=True, max_time_step=10000, reward_objective=1, seed=None, render_mode=None):
        self.num_drivers = num_drivers
        self.num_establishments = num_establishments
        self.num_orders = num_orders
        self.num_costumers = num_costumers
        self.max_time_step = max_time_step

        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode

        self.simpy_env = FoodDeliverySimpyEnv(
            map=GridMap(grid_map_size),
            generators=[
                InitialEstablishmentOrderRateGenerator(self.num_establishments, use_estimate=use_estimate),
                InitialDriverGenerator(self.num_drivers, desconsider_capacity=desconsider_capacity),
                TimeShiftOrderEstablishmentRateGenerator(lambda time: 1, time_shift=4, max_orders=self.num_orders),
            ],
            optimizer=None,
            view=GridViewPygame() if self.render_mode == "human" else None
        )

        self.simpy_env.seed(seed)

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
            'time_to_drivers_complete_order': Box(low=0, high=np.inf, shape=(self.num_drivers, 1), dtype=np.int32),
            'remaining_orders': Discrete(self.num_orders + 1),
            'establishment_busy_time': Box(low=0, high=np.inf, shape=(self.num_establishments, 1), dtype=np.int32),
            'current_time_step': Discrete(max_time_step)
        })

        # Espaço de Ação
        self.action_space = Discrete(self.num_drivers)  # Escolher qual driver pegará o pedido

    def get_observation(self):
        # 1. drivers_busy_time: Tempo de ocupação de cada motorista
        drivers_busy_time = np.zeros((self.num_drivers, 1), dtype=np.int32)
        for i, driver in enumerate(self.simpy_env.state.drivers):
            drivers_busy_time[i] = driver.estimate_total_busy_time()

        # 2. time_to_drivers_complete_order: Tempo estimado para cada motorista completar o próximo pedido
        time_to_drivers_complete_order = np.zeros((self.num_drivers, 1), dtype=np.int32)
        for i, driver in enumerate(self.simpy_env.state.drivers):
            time_to_drivers_complete_order[i] = driver.estimate_time_to_complete_next_order(self.last_order)

        # 3. orders_remaining: Número de pedidos que faltam ser atribuidos a um motorista
        orders_remaining = self.num_orders - self.simpy_env.state.successfully_assigned_routes

        # 4. establishment_next_order_ready_time: Tempo que falta para o próximo pedido em preparação de cada restaurante ficar pronto
        establishment_busy_time = np.zeros((self.num_establishments, 1), dtype=np.int32)
        for i, establishment in enumerate(self.simpy_env.state.establishments):
            establishment_busy_time[i] = establishment.get_establishment_busy_time()

        # 5. current_time_step: O tempo atual da simulação (número do passo)
        current_time_step = self.simpy_env.now

        # Criando a observação final no formato esperado
        obs = {
            'drivers_busy_time': drivers_busy_time,
            'time_to_drivers_complete_order': time_to_drivers_complete_order,
            'remaining_orders': orders_remaining,
            'establishment_busy_time': establishment_busy_time,
            'current_time_step': current_time_step
        }

        return obs
       
    def _get_info(self):
        return {'info': self.simpy_env.now}
    
    def _get_obs(self):
        return self.get_observation()
    
    # Avança na simulação até que um evento principal ocorra ou que a simulação termine/trunque.
    def advance_simulation_until_event(self):
        terminated = False
        truncated = False
        core_event = None

        last_time_step = self.simpy_env.now
        
        while (not terminated) and (not truncated) and (core_event is None):
            if self.simpy_env.state.orders_delivered < self.num_orders:
                self.simpy_env.step()
                self.render()
                
                if last_time_step < self.simpy_env.now:
                    self.print_enviroment_state()
                    last_time_step = self.simpy_env.now

                # Verifica se um pedido foi entregue
                if self.simpy_env.state.orders_delivered > self.last_num_orders_delivered:
                    print("Pedido entregue!")
                    print(f"Número de pedidos entregues: {self.simpy_env.state.orders_delivered}")
                    self.last_num_orders_delivered = self.simpy_env.state.orders_delivered

                # Verifica o próximo evento principal
                core_event = self.simpy_env.dequeue_core_event()

                if core_event is not None:
                    print('\n----> Novo pedido <----')
                    print(core_event.order)
                
                # Verifica se atingiu o limite de tempo
                if self.simpy_env.now >= self.max_time_step:
                    print("Limite de tempo atingido!")
                    truncated = True
            else:
                print("Todos os pedidos foram entregues!")
                terminated = True

        return core_event, terminated, truncated

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.simpy_env.seed(seed)

        if options:
            self.render_mode = options.get("render_mode", None)

        self.simpy_env = FoodDeliverySimpyEnv(
            map=self.simpy_env.map,
            generators=self.simpy_env.generators,
            optimizer=self.simpy_env.optimizer,
            view=GridViewPygame() if self.render_mode == "human" else None
        )

        core_event, _, _ = self.advance_simulation_until_event()
        self.last_order = core_event.order if core_event else None

        observation = self._get_obs()
        info = self._get_info()

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
        
        # Distância total percorrida pelos drivers
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
        # print("action: {}".format(action))
        # print("last_order: {}".format(vars(self.last_order)))
        selected_driver = self.simpy_env.state.drivers[action]
        self.select_driver_to_order(selected_driver, self.last_order)

        core_event, terminated, truncated = self.advance_simulation_until_event()

        self.last_order = core_event.order if core_event else None

        observation = self._get_obs()
        # print(f'observação: {observation}')
        assert self.observation_space.contains(observation), "A observação gerada não está contida no espaço de observação."
        info = self._get_info()

        if terminated or truncated:
            print("Terminated or truncated!")
            reward = 0
            # print(f"reward: {reward}")
            return observation, reward, terminated, truncated, info

        reward = self.calculate_reward(selected_driver)
        # print(f"reward: {reward}")

        return observation, reward, terminated, truncated, info

    def render(self):
        if self.render_mode == "human":
            self.simpy_env.render()

    def show_statistcs_board(self):
        custom_board = CustomBoard(metrics=[
            OrderCurveMetric(self.simpy_env),
            TotalMetric(self.simpy_env),
            DistanceMetric(self.simpy_env),
            DelayMetric(self.simpy_env),
            DriverStatusMetric(self.simpy_env),
            OrderStatusMetric(self.simpy_env),
        ])
        custom_board.view()

    def print_enviroment_state(self, options=None):
        if options is None:
            options = {
                "customers": False,
                "establishments": True,
                "drivers": True,
                "orders": False,
                "events": False,
                "orders_delivered": True
            }
        print(f'time_step = {self.simpy_env.now}')
        self.simpy_env.print_enviroment_state(options)

    def close(self):
        self.simpy_env.close()
