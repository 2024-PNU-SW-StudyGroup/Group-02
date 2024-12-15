import numpy as np
from rl_algorithms.core.algorithms.base import GeneralizedPolicyIteration

class PolicyIteration(GeneralizedPolicyIteration):
    """
    Policy Iteration algorithm implementation.

    This class implements the Policy Iteration algorithm, which alternates
    between policy evaluation and policy improvement steps until the policy
    converges. It is a subclass of `GeneralizedPolicyIteration`.
    """


    def policy_evaluation_step(self) -> float:
        """
        Perform a single policy evaluation step.

        This method computes the state values under the current policy using
        the Bellman expectation equation. It updates the state value estimates
        based on the weighted sum of Q-values for each action, considering the
        current policy probabilities.

        Returns
        -------
        float
            Maximum value change (`delta`) across all states during the
            evaluation step, which serves as a convergence metric.
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

        This method updates the policy by greedily selecting the action with
        the highest Q-value for each state. It checks if the policy has
        converged by comparing the new policy to the old one.

        Returns
        -------
        bool
            True if the policy has converged (no changes were made), False otherwise.
        """
        return self.greedy_policy_improvement()

    def __str__(self) -> str:
        """
        Return a string representation of the algorithm.

        This method provides the name of the algorithm for use in debugging
        or display purposes.

        Returns
        -------
        str
            The name of the algorithm ("Policy Iteration").
        """
        return "Policy Iteration"

    def select_action(self, state: int) -> int:
        """
        Select an action according to the current policy.

        This method samples an action for the given state using the current
        policy's action probabilities.

        Parameters
        ----------
        state : int
            The current state index for which an action is selected.

        Returns
        -------
        int
            The index of the selected action based on the current policy.
        """
        return self.select_policy_action(state)