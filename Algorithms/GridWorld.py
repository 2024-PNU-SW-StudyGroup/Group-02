import numpy as np


class GridWorld:
    def __init__(self, size=7, seed=42):
        # Set random seed
        self.rng = np.random.RandomState(seed)

        self.size = size

        # Define states
        self.n_states = size * size
        """
            It's annoying to consider the states as tuples, so I'll just use the index.
            The index is the row number * size + column number.
            For example, in a 3x3 grid:
            0 1 2
            3 4 5
            6 7 8
        """

        # Define states
        # initial state
        self.initial_state = self.index_to_state(0, 0)
        self.agent_state = self.initial_state
        self.agent_trace = [None, self.agent_state] # comment

        # terminal states
        self.terminal_states = {
            self.index_to_state(size-1, size-1),
            # self.index_to_state(1, 1)
        }

        # walls
        self.walls = {
            self.index_to_state(2, 2),
            self.index_to_state(2, 3),
            self.index_to_state(3, 2)
        }

        # penalty state
        self.penalty_states = {
            self.index_to_state(1, 1),
            self.index_to_state(size-2, size-2)
        }

        # Define actions: up (0), right (1), down (2), left (3)
        self.actions = [0, 1, 2, 3]
        self.action_symbols = ['↑', '→', '↓', '←']

        # Define rewards
        self.rewards = np.zeros(self.n_states)
        self.rewards[[ts for ts in self.terminal_states]] = 1.0
        self.rewards[[ps for ps in self.penalty_states]] = -1.0

        # Transition probability
        self.main_transition_prob = 0.8
        self.transition_probs = np.zeros((self.n_states, len(self.actions), self.n_states))
        # Calculate transition probabilities
        for s in range(self.n_states):
            for a in self.actions:
                for s_prime in self.get_possible_successors(s, a):
                    if s_prime == self.transition(s, a):  # Main movement
                        self.transition_probs[s, a, s_prime] = self.main_transition_prob
                    else:  # Perpendicular movements
                        self.transition_probs[s, a, s_prime] = (1 - self.main_transition_prob) / 2

    def move_agent(self, action):
        self.agent_state = self.transition_w_perp(self.agent_state, action)
        self.agent_trace.append(self.agent_state)
        return self.is_terminated()

    def reset_agent(self):
        self.agent_state = self.initial_state
        self.agent_trace = [None, self.agent_state]

    def is_terminated(self):
        return self.agent_state in self.terminal_states

    def transition_w_perp(self, state, action):
        # print(f"selected action: {self.action_symbols[action]}", end=' ')

        if self.rng.rand() > self.main_transition_prob:
            perp_action1 = (action + 1) % 4
            perp_action2 = (action - 1) % 4
            action = self.rng.choice([perp_action1, perp_action2])
        #     print(f"| Perpendicular action: {self.action_symbols[action]}")
        # else:
        #     print()
        return self.transition(state, action)

    def get_possible_successors(self, state: int, action: int) -> list:
        "Return a list of possible successor states given a state and action considering walls, boundaries, and perpendicular movements."
        successors = set()

        # Main movement
        main_successor = self.transition(state, action)
        successors.add(main_successor)

        # Perpendicular movements
        perp_action1 = (action + 1) % 4
        perp_action2 = (action - 1) % 4
        perp_successor1 = self.transition(state, perp_action1)
        perp_successor2 = self.transition(state, perp_action2)
        successors.add(perp_successor1)
        successors.add(perp_successor2)

        return successors

    def transition(self, state: int, action: int) -> int:
        i, j = self.state_to_index(state)
        if action == 0:  # up
            i = i - 1
        elif action == 1:  # right
            j = j + 1
        elif action == 2:  # down
            i = i + 1
        elif action == 3:  # left
            j = j - 1
        next_state = self.index_to_state(i, j)

        if next_state in self.walls or i < 0 or i >= self.size or j < 0 or j >= self.size:
            return state

        return next_state

    def state_to_index(self, state: int) -> tuple: # index_to_coord
        return (state // self.size, state % self.size)

    def index_to_state(self, index_or_i, j=None) -> int: # coord_to_index
        if isinstance(index_or_i, tuple): # i, j are passed as a tuple
            i, j = index_or_i
        else: # i, j are passed as separate arguments
            i = index_or_i
        return i * self.size + j
