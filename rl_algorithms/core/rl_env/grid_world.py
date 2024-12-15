import numpy as np

class GridWorld:
    """
    A GridWorld environment for reinforcement learning experiments.

    The environment is a grid where an agent navigates between cells,
    encountering terminal states, walls, and penalty states.
    The agent receives rewards or penalties depending on its state.

    Parameters
    ----------
    size : int, optional
        The size of the grid (default is 7).
    seed : int, optional
        The random seed for reproducibility (default is 42).

    Attributes
    ----------
    size : int
        The size of the grid.
    n_states : int
        Total number of states in the grid (size x size).
    initial_state : int
        The initial state of the agent.
    agent_state : int
        The current state of the agent.
    agent_trace : list of int
        The trace of agent's past states.
    terminal_states : set of int
        The set of terminal states.
    walls : set of int
        The set of wall states.
    penalty_states : set of int
        The set of penalty states.
    actions : list of int
        The available actions (0: up, 1: right, 2: down, 3: left).
    action_symbols : list of str
        The symbols representing each action.
    rewards : ndarray of float
        The rewards for each state.
    main_transition_prob : float
        The probability of the agent taking the intended action.
    transition_probs : ndarray of float
        The transition probabilities for each state and action.

    Methods
    -------
    move_agent(action)
        Move the agent according to the specified action.
    reset_agent()
        Reset the agent to its initial state.
    is_terminated()
        Check if the agent has reached a terminal state.
    transition_w_perp(state, action)
        Perform a transition with perpendicular movement.
    get_possible_successors(state, action)
        Get all possible successor states for a given state and action.
    transition(state, action)
        Compute the next state based on the current state and action.
    state_to_index(state)
        Convert a state index to its grid coordinates (row, column).
    index_to_state(index_or_i, j=None)
        Convert grid coordinates (row, column) to a state index.
    """

    def __init__(self, size=7, seed=42):
        """
        Initialize the GridWorld environment.

        Parameters
        ----------
        size : int, optional
            The size of the grid (default is 7).
        seed : int, optional
            The random seed for reproducibility (default is 42).
        """
        self.rng = np.random.RandomState(seed)
        self.size = size
        self.n_states = size * size

        self.initial_state = self.index_to_state(0, 0)
        self.agent_state = self.initial_state
        self.agent_trace = [None, self.agent_state]

        self.terminal_states = {
            self.index_to_state(size - 1, size - 1),
        }

        self.walls = {
            self.index_to_state(2, 2),
            self.index_to_state(2, 3),
            self.index_to_state(3, 2),
        }

        self.penalty_states = {
            self.index_to_state(1, 1),
            self.index_to_state(size - 2, size - 2),
        }

        self.actions = [0, 1, 2, 3]
        self.action_symbols = ['↑', '→', '↓', '←']

        self.rewards = np.zeros(self.n_states)
        self.rewards[[ts for ts in self.terminal_states]] = 1.0
        self.rewards[[ps for ps in self.penalty_states]] = -1.0

        self.main_transition_prob = 0.8
        self.transition_probs = np.zeros((self.n_states, len(self.actions), self.n_states))

        for s in range(self.n_states):
            for a in self.actions:
                for s_prime in self.get_possible_successors(s, a):
                    if s_prime == self.transition(s, a):
                        self.transition_probs[s, a, s_prime] = self.main_transition_prob
                    else:
                        self.transition_probs[s, a, s_prime] = (1 - self.main_transition_prob) / 2

    def move_agent(self, action):
        """
        Move the agent according to the specified action.

        Parameters
        ----------
        action : int
            The action to take (0: up, 1: right, 2: down, 3: left).

        Returns
        -------
        bool
            True if the agent reaches a terminal state, False otherwise.
        """
        self.agent_state = self.transition_w_perp(self.agent_state, action)
        self.agent_trace.append(self.agent_state)
        return self.is_terminated()

    def reset_agent(self):
        """
        Reset the agent to its initial state.
        """
        self.agent_state = self.initial_state
        self.agent_trace = [None, self.agent_state]

    def is_terminated(self):
        """
        Check if the agent has reached a terminal state.

        Returns
        -------
        bool
            True if the agent is in a terminal state, False otherwise.
        """
        return self.agent_state in self.terminal_states

    def transition_w_perp(self, state, action):
        """
        Perform a transition with possible perpendicular movement.

        Parameters
        ----------
        state : int
            The current state.
        action : int
            The action to take (0: up, 1: right, 2: down, 3: left).

        Returns
        -------
        int
            The resulting state after the action.
        """
        if self.rng.rand() > self.main_transition_prob:
            perp_action1 = (action + 1) % 4
            perp_action2 = (action - 1) % 4
            action = self.rng.choice([perp_action1, perp_action2])
        return self.transition(state, action)

    def get_possible_successors(self, state: int, action: int) -> list:
        """
        Get all possible successor states for a given state and action.

        Parameters
        ----------
        state : int
            The current state.
        action : int
            The action to take (0: up, 1: right, 2: down, 3: left).

        Returns
        -------
        list of int
            The list of possible successor states.
        """
        successors = set()
        successors.add(self.transition(state, action))
        perp_action1 = (action + 1) % 4
        perp_action2 = (action - 1) % 4
        successors.add(self.transition(state, perp_action1))
        successors.add(self.transition(state, perp_action2))
        return list(successors)

    def transition(self, state: int, action: int) -> int:
        """
        Compute the next state based on the current state and action.

        Parameters
        ----------
        state : int
            The current state.
        action : int
            The action to take (0: up, 1: right, 2: down, 3: left).

        Returns
        -------
        int
            The next state after the action.
        """
        i, j = self.state_to_index(state)
        if action == 0:
            i -= 1
        elif action == 1:
            j += 1
        elif action == 2:
            i += 1
        elif action == 3:
            j -= 1
        next_state = self.index_to_state(i, j)
        if next_state in self.walls or i < 0 or i >= self.size or j < 0 or j >= self.size:
            return state
        return next_state

    def state_to_index(self, state: int) -> tuple:
        """
        Convert a state index to its grid coordinates.

        Parameters
        ----------
        state : int
            The state index.

        Returns
        -------
        tuple of int
            The grid coordinates (row, column).
        """
        return state // self.size, state % self.size

    def index_to_state(self, index_or_i, j=None) -> int:
        """
        Convert grid coordinates to a state index.

        Parameters
        ----------
        index_or_i : int or tuple of int
            The row index or a tuple of (row, column).
        j : int, optional
            The column index if `index_or_i` is an integer.

        Returns
        -------
        int
            The state index.
        """
        if isinstance(index_or_i, tuple):
            i, j = index_or_i
        else:
            i = index_or_i
        return i * self.size + j