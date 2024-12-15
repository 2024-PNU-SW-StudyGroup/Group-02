import numpy as np
from rl_algorithms.core.algorithms.base import GeneralizedPolicyIteration

class ValueIteration(GeneralizedPolicyIteration):
    """
    Value Iteration algorithm implementation.

    Inherits from GeneralizedPolicyIteration and overrides the policy evaluation
    step to use the Bellman optimality update. This algorithm repeatedly updates
    state values to the maximum Q-value over all actions until convergence.
    """

    def policy_evaluation_step(self) -> float:
        """
        Perform a single value iteration step.

        This method computes the Q-values for each state-action pair using the
        Bellman optimality equation, then updates the state value to the maximum
        Q-value over all actions. The maximum absolute difference (`delta`)
        between old and updated values is returned as a convergence metric.

        Returns
        -------
        float
            The maximum value change (delta) across all states during this iteration step.
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

        This method calls a greedy improvement procedure (`greedy_policy_improvement`)
        which sets the action probability to 1 for the action with the highest Q-value,
        and 0 otherwise.

        Returns
        -------
        bool
            True if the policy did not change (converged), False otherwise.
        """
        return self.greedy_policy_improvement()

    def __str__(self) -> str:
        """
        Returns a string representation of this algorithm.

        Returns
        -------
        str
            Name of the algorithm ("Value Iteration").
        """

        return "Value Iteration"

    def select_action(self, state: int) -> int:
        """
        Select a greedy action based on the current Q-values.

        Uses `select_greedy_action` to pick the action that maximizes Q(s,a).

        Parameters
        ----------
        state : int
            Current state index.

        Returns
        -------
        int
            The selected (greedy) action index.
        """
        return self.select_greedy_action(state)