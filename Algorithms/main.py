import numpy as np
import pygame
from GridWorld import GridWorld
from RLAlgorithms import PolicyIteration, ValueIteration  # , QLearning
from UI import GridWorldViz


def main(seed=42):
    # Create environment with seed
    env = GridWorld(size=7, seed=seed)

    # Create algorithms with seed
    algorithms = [
        PolicyIteration(env, gamma=0.9, seed=seed),
        ValueIteration(env, gamma=0.9, seed=seed),
        # 'q_learning': QLearning(env, gamma=0.9, alpha=0.1, epsilon=0.1, seed=seed)
    ]

    # Create and run visualization
    viz = GridWorldViz(env, algorithms)
    viz.run()


if __name__ == "__main__":
    # Set global numpy seed for any remaining random operations
    np.random.seed(42)
    main(seed=42)
