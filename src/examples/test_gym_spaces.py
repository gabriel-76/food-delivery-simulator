import numpy as np
from gymnasium.spaces import Discrete, Box, Tuple, MultiDiscrete, Sequence, Dict


def run():
    # box_space = Box(low=-1.0, high=2.0, shape=(3, 2), dtype=np.float32)
    # box_space = Box(low=np.array([[-1.0, -2.0],[-1.0, -2.0]]), high=np.array([[2.0, 4.0],[2.0, 4.0]]), shape=(2,2), dtype=np.float32)
    # box_space = Box(low=-np.inf, high=np.inf, shape=(10, 2), dtype=np.float32)
    # box_sample = box_space.sample()
    # print(box_sample)
    # # contains_e = box_space.contains([0.5122504, -0.9937976])
    # # print(contains_e)
    # print()
    #
    # discrete_space = Discrete(10, start=-10)  # {0, 1}
    # discrete_sample = discrete_space.sample()
    # print(discrete_sample)
    # print()
    #
    # multi_discrete_space = MultiDiscrete([[10, 2], [5, 9]])
    # multi_discrete_sample = multi_discrete_space.sample()
    # print(multi_discrete_sample)
    # print()
    #
    # tuple_space = Tuple((
    #     Discrete(10),
    #     MultiDiscrete([20] * 10)
    # ))
    # tuple_sample = tuple_space.sample()
    # print(tuple_sample)
    #
    # contains = tuple_space.contains((1, [5, 9, 2, 12, 2, 1, 8, 7, 5]))
    # print(contains)
    # print()
    #
    # sequence_space = Sequence(Discrete(100, start=0))
    # sequence_sample = sequence_space.sample()
    # print(sequence_sample)
    # print()
    #
    # action_space = Sequence(
    #     Tuple((
    #         Discrete(10),
    #         Sequence(Discrete(100, start=0))
    #     ))
    # )
    # s = action_space.sample()
    # print(s)

    observation_space = Dict({
        'num_drivers': Discrete(10000),  # {0, 1, 2, ..., inf} -> 'num_drivers'
        'drivers': Sequence(
            Dict({
                'coordinates': Box(low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32),  # (x, y)
                'available': Discrete(2),  # {0, 1} -> {false or true}
                'capacity': Discrete(10000000000),  # {0, 1, 2, ..., inf} -> capacity
                'status': Discrete(3),  # {0, 1, 2} -> {AVAILABLE, PICKING_UP, DELIVERING}
                'current_route': Sequence(Box(low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32))
                # [(x, y), (x, y), ...]
            })
        ),
        'num_orders': Discrete(10000),  # {0, 1, 2, ..., inf} -> 'num_orders
        'orders': Sequence(Dict({
            'pickup_coordinate': Box(low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32),  # (x, y)
            'delivery_coordinate': Box(low=-np.inf, high=np.inf, shape=(2,), dtype=np.float32),  # (x, y)
            'status': Discrete(13),  # {0, 1, 2, ... 12} -> order.status
            'required_capacity': Discrete(10000000000),  # {0, 1, 2, ..., inf} -> required_capacity
        }))
    })

    observation_sample = observation_space.sample()
    print(observation_sample)

    contains = observation_space.contains({'num_drivers': 1, 'drivers': ({'coordinates': [58.0, 25.0], 'available': 1, 'capacity': 100000000, 'status': 1, 'current_route': ()},), 'num_orders': 0, 'orders': ()})
    print(contains)


if __name__ == '__main__':
    run()
