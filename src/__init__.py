import simpy

from src.simulator.simulator import Simulator

SIMULATION_TIME = 20


def main():
    env = simpy.Environment()
    simulator = Simulator(env)
    simulator.run()
    env.run(until=SIMULATION_TIME)


if __name__ == '__main__':
    main()
