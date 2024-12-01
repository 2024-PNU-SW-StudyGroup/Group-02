import numpy as np
from .base import GeneralizedPolicyIteration

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