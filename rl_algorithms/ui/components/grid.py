# ui/components/grid.py
import pygame

class GridComponent:
    """
    A component for rendering the Grid World environment and agent in a visualization.

    Attributes
    ----------
    viz : object
        The visualization object that holds the environment and other settings.
    cell_size : int
        The size of each cell in the grid.
    font : pygame.font.Font
        The font used for rendering text in the grid.
    BLACK, WHITE, GRAY, RED, GREEN, BLUE : tuple
        RGB color values for drawing elements in the grid.
    """
    def __init__(self, viz, cell_size, font, colors):
        """
        Initializes the grid component with visualization settings.

        Parameters
        ----------
        viz : object
            The visualization object that contains the environment.
        cell_size : int
            The size of each cell in the grid.
        font : pygame.font.Font
            The font to be used for rendering text in the grid.
        colors : dict
            A dictionary containing RGB color values for different elements.
        """
        self.viz = viz
        self.cell_size = cell_size
        self.font = font
        self.BLACK = colors['BLACK']
        self.WHITE = colors['WHITE']
        self.GRAY = colors['GRAY']
        self.RED = colors['RED']
        self.GREEN = colors['GREEN']
        self.BLUE = colors['BLUE']

    def draw(self, screen, show_rewards, show_state_values, show_action_values, show_policy, current_alg):
        """
        Renders the grid, agent, and any overlays like rewards, state values, or policy.

        Parameters
        ----------
        screen : pygame.Surface
            The pygame surface to draw on.
        show_rewards : bool
            Whether to display rewards in each cell.
        show_state_values : bool
            Whether to display state values in each cell.
        show_action_values : bool
            Whether to display action values in each cell.
        show_policy : bool
            Whether to display policy arrows in each cell.
        current_alg : object
            The currently selected reinforcement learning algorithm.
        """
        env = self.viz.env
        for i in range(env.size):
            for j in range(env.size):
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                                   self.cell_size, self.cell_size)
                s = env.index_to_state(i, j)
                self.draw_cell_background(screen, rect, s)
                if show_rewards:
                    self.draw_rewards(screen, rect, s)
                if current_alg is not None and show_state_values:
                    self.draw_state_values(screen, rect, s, current_alg)
                if current_alg is not None and show_action_values:
                    self.draw_action_values(screen, rect, s, current_alg)
                if current_alg is not None and show_policy:
                    self.draw_policy_arrows(screen, rect, s, current_alg)

        self.draw_agent(screen)

    def draw_cell_background(self, screen, rect, s):
        """
        Draws the background of a single cell in the grid.

        Parameters
        ----------
        screen : pygame.Surface
            The pygame surface to draw on.
        rect : pygame.Rect
            The rectangle defining the cell's position and size.
        s : int
            The state index of the cell.
        """
        env = self.viz.env
        if s in env.terminal_states:
            color = self.GREEN if env.rewards[s] > 0 else self.RED
        elif s in env.walls:
            color = self.GRAY
        elif s in env.penalty_states:
            color = self.RED
        else:
            color = self.WHITE
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, self.BLACK, rect, 1)

    def draw_rewards(self, screen, rect, s):
        """
        Draws the reward value in a cell.

        Parameters
        ----------
        screen : pygame.Surface
            The pygame surface to draw on.
        rect : pygame.Rect
            The rectangle defining the cell's position and size.
        s : int
            The state index of the cell.
        """
        text = self.font.render(f'{self.viz.env.rewards[s]:.1f}', True, self.BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    def draw_state_values(self, screen, rect, s, current_alg):
        """
        Draws the state value in a cell.

        Parameters
        ----------
        screen : pygame.Surface
            The pygame surface to draw on.
        rect : pygame.Rect
            The rectangle defining the cell's position and size.
        s : int
            The state index of the cell.
        current_alg : object
            The currently selected reinforcement learning algorithm.
        """
        v_s = current_alg.values[s]
        text = self.font.render(f'{v_s:.2f}', True, self.BLACK)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    def draw_action_values(self, screen, rect, s, current_alg):
        """
        Draws the action values in a cell.

        Parameters
        ----------
        screen : pygame.Surface
            The pygame surface to draw on.
        rect : pygame.Rect
            The rectangle defining the cell's position and size.
        s : int
            The state index of the cell.
        current_alg : object
            The currently selected reinforcement learning algorithm.
        """
        env = self.viz.env
        for a in env.actions:
            q_sa = current_alg.q_values[s, a]
            text = self.font.render(f'{q_sa:.2f}', True, self.BLACK)
            if a == 0:
                text_rect = text.get_rect(midtop=rect.midtop)
            elif a == 1:
                text_rect = text.get_rect(midright=rect.midright)
            elif a == 2:
                text_rect = text.get_rect(midbottom=rect.midbottom)
            elif a == 3:
                text_rect = text.get_rect(midleft=rect.midleft)
            screen.blit(text, text_rect)

    def draw_policy_arrows(self, screen, rect, s, current_alg):
        """
        Draws policy arrows in a cell.

        Parameters
        ----------
        screen : pygame.Surface
            The pygame surface to draw on.
        rect : pygame.Rect
            The rectangle defining the cell's position and size.
        s : int
            The state index of the cell.
        current_alg : object
            The currently selected reinforcement learning algorithm.
        """
        policy_probs = current_alg.policy[s]
        env = self.viz.env
        selected_action = self.viz.control_section.selected_action
        for a, prob in enumerate(policy_probs):
            if prob > 0:
                start_pos, end_pos = self.get_arrow_positions(rect, a)
                color = self.RED if (len(env.agent_trace) > 1 and s == env.agent_trace[-2] and a == selected_action) else self.BLACK
                self.draw_arrow(screen, a, start_pos, end_pos, color)

    def get_arrow_positions(self, rect, a):
        """
        Gets the start and end positions for drawing an arrow based on action.

        Parameters
        ----------
        rect : pygame.Rect
            The rectangle defining the cell's position and size.
        a : int
            The action index (0: Up, 1: Right, 2: Down, 3: Left).

        Returns
        -------
        tuple
            A tuple of start and end positions for the arrow.
        """
        if a == 0:  # Up
            start_pos = (rect.centerx, rect.centery - self.cell_size // 4)
            end_pos = (rect.centerx, rect.centery - self.cell_size // 2)
        elif a == 1:  # Right
            start_pos = (rect.centerx + self.cell_size // 4, rect.centery)
            end_pos = (rect.centerx + self.cell_size // 2, rect.centery)
        elif a == 2:  # Down
            start_pos = (rect.centerx, rect.centery + self.cell_size // 4)
            end_pos = (rect.centerx, rect.centery + self.cell_size // 2)
        elif a == 3:  # Left
            start_pos = (rect.centerx - self.cell_size // 4, rect.centery)
            end_pos = (rect.centerx - self.cell_size // 2, rect.centery)
        return start_pos, end_pos

    def draw_arrow(self, screen, direction, start_pos, end_pos, color, width=2):
        """
        Draws an arrow indicating a policy or action.

        Parameters
        ----------
        screen : pygame.Surface
            The pygame surface to draw on.
        direction : int
            The direction of the arrow (0: Up, 1: Right, 2: Down, 3: Left).
        start_pos : tuple
            The starting position of the arrow.
        end_pos : tuple
            The ending position of the arrow.
        color : tuple
            The color of the arrow.
        width : int, optional
            The width of the arrow line, by default 2.
        """
        pygame.draw.line(screen, color, start_pos, end_pos, width)
        if direction == 0:
            pygame.draw.polygon(screen, color, [(end_pos[0] - 5, end_pos[1] + 5),
                                                end_pos,
                                                (end_pos[0] + 5, end_pos[1] + 5)])
        elif direction == 1:
            pygame.draw.polygon(screen, color, [(end_pos[0] - 5, end_pos[1] - 5),
                                                end_pos,
                                                (end_pos[0] - 5, end_pos[1] + 5)])
        elif direction == 2:
            pygame.draw.polygon(screen, color, [(end_pos[0] - 5, end_pos[1] - 5),
                                                end_pos,
                                                (end_pos[0] + 5, end_pos[1] - 5)])
        elif direction == 3:
            pygame.draw.polygon(screen, color, [(end_pos[0] + 5, end_pos[1] - 5),
                                                end_pos,
                                                (end_pos[0] + 5, end_pos[1] + 5)])

    def draw_agent(self, screen):
        """
        Draws the agent's current position in the grid.

        Parameters
        ----------
        screen : pygame.Surface
            The pygame surface to draw on.
        """
        env = self.viz.env
        agent_pos = env.state_to_index(env.agent_state)
        agent_center = (agent_pos[1] * self.cell_size + self.cell_size // 2,
                        agent_pos[0] * self.cell_size + self.cell_size // 2)
        pygame.draw.circle(screen, self.BLUE, agent_center, self.cell_size//4)

    def update_agent(self, agent_data):
        """
        Updates the agent's state in response to a movement event.

        Parameters
        ----------
        agent_data : dict
            Data about the agent's movement, including:
            - `action` (int): The action taken by the agent.
            - `state` (int): The resulting state of the agent.
            - `done` (bool): Whether the agent has reached a terminal state.
        """
        pass