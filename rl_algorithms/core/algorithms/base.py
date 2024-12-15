from abc import ABC, abstractmethod
import numpy as np
from core.rl_env.grid_world import GridWorld


class RLAlgorithm(ABC):
    """Base class for Reinforcement Learning algorithms."""

    def __init__(self, env: GridWorld, gamma: float = 0.9, seed: int = 42):
        """
        Initialize the Reinforcement Learning algorithm.

        Args:
            env (GridWorld): The environment to interact with
            gamma (float): Discount factor for future rewards
            seed (int): Random seed for reproducibility
        """
        self.env = env
        self.gamma = gamma
        self.rng = np.random.RandomState(seed)
        self.reset()

    def reset(self) -> None:
        """
        Reset the algorithm's internal state:
        - Initialize value function to zeros
        - Set uniform initial policy
        - Reset Q-values to zeros
        """
        self.values = np.zeros(self.env.n_states)
        # Uniform initial policy
        self.policy = np.full(
            (self.env.n_states, len(self.env.actions)),
            1.0 / len(self.env.actions)
        )
        self.q_values = np.zeros((self.env.n_states, len(self.env.actions)))

    def set_seed(self, seed: int) -> None:
        """
        Reset the random number generator with a new seed.

        Args:
            seed (int): New random seed
        """
        self.rng = np.random.RandomState(seed)

    def __str__(self) -> str:
        """Subclasses must provide a string representation."""
        raise NotImplementedError

    def move_agent(self, action: int):
        """
        Move the agent according to the current policy.

        Args:
            action (int): Action to take
        """
        return self.env.move_agent(action)

    def reset_agent(self) -> None:
        """Reset the agent to its initial state."""
        self.env.reset_agent()

    def select_action(self, state: int):
        """
        Select an action for a given state.

        Args:
            state (int): Current state

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError

    def select_policy_action(self, state: int) -> int: # select_stochastic_action
        """
        Select an action based on the current policy using random sampling.

        Args:
            state (int): Current state

        Returns:
            int: Selected action
        """
        return self.rng.choice(self.env.actions, p=self.policy[state])

    def select_greedy_action(self, state: int) -> int:
        """
        Select the action with the highest probability in the policy.

        Args:
            state (int): Current state

        Returns:
            int: Action with highest probability
        """
        return np.argmax(self.policy[state])


class GeneralizedPolicyIteration(RLAlgorithm):
    """Base class for Generalized Policy Iteration algorithms."""

    def policy_evaluation_step(self, theta: float = 1e-6) -> float:
        """
        Single step of policy evaluation.

        Args:
            theta (float): Convergence threshold

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError

    def policy_improvement_step(self) -> bool:
        """
        Single step of policy improvement.

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError

    def greedy_policy_improvement(self) -> bool:
        """
        Improve policy greedily based on current Q-values.

        Returns:
            bool: Whether the policy has converged
        """
        is_policy_converged = True
        for s in range(self.env.n_states):
            if s in self.env.terminal_states:
                continue

            old_policy = self.policy[s].copy()

            # Reset policy probabilities
            self.policy[s] = np.zeros(len(self.env.actions))

            # Select best action
            best_action = np.argmax(self.q_values[s])
            self.policy[s, best_action] = 1

            # Check if policy changed
            if not np.array_equal(old_policy, self.policy[s]):
                is_policy_converged = False

        return is_policy_converged

    def step(self) -> bool:
        """
        Single step of generalized policy iteration.

        Returns:
            bool: Whether the algorithm has converged
        """
        self.policy_evaluation_step()
        return self.policy_improvement_step()

    def run(self, max_steps: int = 1000) -> None:
        """
        Run generalized policy iteration until convergence.

        Args:
            max_steps (int): Maximum number of iteration steps
        """
        for _ in range(max_steps):
            is_converged = self.step()
            if is_converged:
                break