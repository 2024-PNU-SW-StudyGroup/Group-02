import numpy as np
from core.env.grid_world import GridWorld
from core.algorithms.policy_iteration import PolicyIteration
from core.algorithms.value_iteration import ValueIteration
from ui.grid_world_viz import GridWorldViz

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
