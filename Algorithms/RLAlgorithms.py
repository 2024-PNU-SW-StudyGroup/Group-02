import numpy as np
from typing import List, Optional
from GridWorld import GridWorld


class RLAlgorithm:
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


class PolicyIteration(GeneralizedPolicyIteration):
    """Policy Iteration algorithm implementation."""

    def policy_evaluation_step(self) -> float:
        """
        Perform a single policy evaluation step.

        Returns:
            float: Maximum value change during evaluation
        """
        delta = 0
        old_values = self.values.copy()

        for s in range(self.env.n_states):
            # Skip terminal and wall states
            if s in self.env.terminal_states or s in self.env.walls:
                continue

            # Compute state value under current policy
            v = 0
            for a in self.env.actions:
                q = 0
                for s_prime in self.env.get_possible_successors(s, a):
                    # Bellman expectation equation
                    q += (self.env.transition_probs[s, a, s_prime] *
                          (self.env.rewards[s_prime] + self.gamma * old_values[s_prime]))

                # Store Q-values
                self.q_values[s, a] = q
                # Weighted sum by policy probabilities
                v += self.policy[s, a] * q

            # Update state value
            self.values[s] = v
            # Track maximum value change
            delta = max(delta, np.abs(old_values[s] - self.values[s]))

        return delta

    def policy_improvement_step(self) -> bool:
        """
        Improve policy based on current value estimates.

        Returns:
            bool: Whether the policy has converged
        """
        return self.greedy_policy_improvement()

    def __str__(self) -> str:
        return "Policy Iteration"

    def select_action(self, state: int) -> int:
        """
        Select action according to current policy.

        Args:
            state (int): Current state

        Returns:
            int: Selected action
        """
        return self.select_policy_action(state)


class ValueIteration(GeneralizedPolicyIteration):
    """Value Iteration algorithm implementation."""

    def policy_evaluation_step(self) -> float:
        """
        Perform a single value iteration step.

        Returns:
            float: Maximum value change during iteration
        """
        delta = 0
        old_values = self.values.copy()

        for s in range(self.env.n_states):
            # Skip terminal and wall states
            if s in self.env.terminal_states or s in self.env.walls:
                continue

            # Compute maximum Q-value across all actions
            q_values = []
            for a in self.env.actions:
                q = 0
                for s_prime in self.env.get_possible_successors(s, a):
                    # Bellman optimality equation
                    q += (self.env.transition_probs[s, a, s_prime] *
                          (self.env.rewards[s_prime] + self.gamma * old_values[s_prime]))
                q_values.append(q)

            # Update Q-values and state value
            self.q_values[s] = q_values
            self.values[s] = max(q_values)

            # Track maximum value change
            delta = max(delta, np.abs(old_values[s] - self.values[s]))

        return delta

    def policy_improvement_step(self) -> bool:
        """
        Improve policy based on current value estimates.

        Returns:
            bool: Whether the policy has converged
        """
        return self.greedy_policy_improvement()

    def __str__(self) -> str:
        return "Value Iteration"

    def select_action(self, state: int) -> int:
        """
        Select greedy action based on current Q-values.

        Args:
            state (int): Current state

        Returns:
            int: Selected action
        """
        return self.select_greedy_action(state)
