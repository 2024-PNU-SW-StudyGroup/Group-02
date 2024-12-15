from abc import ABC, abstractmethod
import numpy as np
from core.rl_env.grid_world import GridWorld


class RLAlgorithm(ABC):
    """
    Base class for Reinforcement Learning algorithms.

    This abstract base class provides the common structure and functionality
    for all reinforcement learning algorithms. It includes methods for resetting
    the internal state, setting a random seed, and managing agent actions and policies.

    Attributes
    ----------
    env : GridWorld
        The environment the algorithm interacts with.
    gamma : float
        Discount factor for future rewards.
    rng : np.random.RandomState
        Random number generator for reproducibility.
    values : np.ndarray
        Array representing the value function of each state.
    policy : np.ndarray
        Array representing the current policy probabilities for each state-action pair.
    q_values : np.ndarray
        Array representing the Q-values for each state-action pair.
    """

    def __init__(self, env: GridWorld, gamma: float = 0.9, seed: int = 42):
        """
        Initialize the Reinforcement Learning algorithm.

        Parameters
        ----------
        env : GridWorld
            The environment to interact with.
        gamma : float, optional
            Discount factor for future rewards (default is 0.9).
        seed : int, optional
            Random seed for reproducibility (default is 42).
        """
        self.env = env
        self.gamma = gamma
        self.rng = np.random.RandomState(seed)
        self.reset()

    def reset(self) -> None:
        """
        Reset the algorithm's internal state.

        This method initializes the value function to zeros, sets the initial
        policy to a uniform distribution, and resets the Q-values to zeros.

        Returns
        -------
        None
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

        Parameters
        ----------
        seed : int
            New random seed.

        Returns
        -------
        None
        """
        self.rng = np.random.RandomState(seed)

    def __str__(self) -> str:
        """
        Return a string representation of the algorithm.

        Returns
        -------
        str
            Name of the algorithm.

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this method.
        """
        raise NotImplementedError

    def move_agent(self, action: int):
        """
        Move the agent according to the current policy.

        Parameters
        ----------
        action : int
            Action to take.

        Returns
        -------
        Any
            Result of the environment's `move_agent` method.
        """
        return self.env.move_agent(action)

    def reset_agent(self) -> None:
        """
        Reset the agent to its initial state.

        This method calls the environment's `reset_agent` method.

        Returns
        -------
        None
        """
        self.env.reset_agent()

    def select_action(self, state: int):
        """
        Select an action for a given state.

        This method must be implemented by subclasses to define how
        an action is selected.

        Parameters
        ----------
        state : int
            Current state index.

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this method.
        """
        raise NotImplementedError

    def select_policy_action(self, state: int) -> int: # select_stochastic_action
        """
        Select an action based on the current policy using random sampling.

        Parameters
        ----------
        state : int
            Current state index.

        Returns
        -------
        int
            Selected action index.
        """
        return self.rng.choice(self.env.actions, p=self.policy[state])

    def select_greedy_action(self, state: int) -> int:
        """
        Select the action with the highest probability in the policy.

        Parameters
        ----------
        state : int
            Current state index.

        Returns
        -------
        int
            Action with the highest probability.
        """
        return np.argmax(self.policy[state])


class GeneralizedPolicyIteration(RLAlgorithm):
    """
    Base class for Generalized Policy Iteration algorithms.

    This class provides the structure for algorithms that alternate between
    policy evaluation and policy improvement steps.
    """

    def policy_evaluation_step(self, theta: float = 1e-6) -> float:
        """
        Single step of policy evaluation.

        Parameters
        ----------
        theta : float, optional
            Convergence threshold (default is 1e-6).

        Returns
        -------
        float
            Maximum value change (`delta`) during evaluation step.

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this method.
        """
        raise NotImplementedError

    def policy_improvement_step(self) -> bool:
        """
        Single step of policy improvement.

        Returns
        -------
        bool
            True if the policy has converged, False otherwise.

        Raises
        ------
        NotImplementedError
            If the subclass does not implement this method.
        """
        raise NotImplementedError

    def greedy_policy_improvement(self) -> bool:
        """
        Improve the policy greedily based on current Q-values.

        This method sets the action probability to 1 for the action with the
        highest Q-value and 0 for others. It checks if the new policy is the
        same as the old one.

        Returns
        -------
        bool
            True if the policy has converged, False otherwise.
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

        This step includes a policy evaluation followed by a policy
        improvement. It checks if the policy has converged.

        Returns
        -------
        bool
            True if the policy has converged, False otherwise.
        """
        self.policy_evaluation_step()
        return self.policy_improvement_step()

    def run(self, max_steps: int = 1000) -> None:
        """
        Run generalized policy iteration until convergence.

        This method alternates between policy evaluation and policy
        improvement steps until the policy converges or the maximum
        number of steps is reached.

        Parameters
        ----------
        max_steps : int, optional
            Maximum number of iteration steps (default is 1000).

        Returns
        -------
        None
        """
        for _ in range(max_steps):
            is_converged = self.step()
            if is_converged:
                break