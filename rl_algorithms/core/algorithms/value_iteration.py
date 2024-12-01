import numpy as np
from .base import GeneralizedPolicyIteration

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