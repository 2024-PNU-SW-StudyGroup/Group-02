import pygame
import numpy as np
import sys
from RLAlgorithms import PolicyIteration, ValueIteration  # , QLearning


class GridWorldViz:
    def __init__(self, env, algorithms):
        pygame.init()

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)

        # Display settings
        self.CELL_SIZE = 125

        self.env = env
        self.font = pygame.font.Font(None, 24)

        # Agent Circle
        self.agent_radius = self.CELL_SIZE // 4

        # Button dimensions
        self.button_width = 280
        self.button_height = 40

        # Algorithm selection section
        self.algorithms = algorithms
        self.current_alg = None

        self.algo_sec_left = env.size * self.CELL_SIZE
        self.algo_sec_left_edge = self.algo_sec_left
        self.algo_sec_button_left = self.algo_sec_left + 20

        self.algo_sec_title = {'text': 'Select Algorithm', 'rect': pygame.Rect(
            self.algo_sec_button_left, 20, self.button_width, self.button_height)}
        # Algorithm selection buttons
        self.algo_buttons = [
            {'text': f'{algo}', 'rect': pygame.Rect(self.algo_sec_button_left, 20 + (i + 1) * 50, self.button_width, self.button_height)} for i, algo in enumerate(algorithms)
        ]

        # Visualization configuration section
        self.show_rewards = True
        self.show_state_values = False
        self.show_action_values = False
        self.show_policy = False

        self.viz_sec_left = self.algo_sec_left + 20 + self.button_width + 20
        self.viz_sec_left_edge = self.viz_sec_left
        self.viz_sec_button_left = self.viz_sec_left + 20

        self.viz_sec_title = {'text': 'Toggle Vizualizaion', 'rect': pygame.Rect(
            self.viz_sec_button_left, 20, self.button_width, self.button_height)}

        # Visualization configuration buttons
        self.viz_config_buttons = [
            {'text': 'Toggle Rewards', 'rect': pygame.Rect(
                self.viz_sec_button_left, 20 + 50, self.button_width, self.button_height), 'state': True, 'visible': True},
            {'text': 'Toggle State Values', 'rect': pygame.Rect(
                self.viz_sec_button_left, 20 + 100, self.button_width, self.button_height), 'state': False, 'visible': False},
            {'text': 'Toggle Action Values', 'rect': pygame.Rect(
                self.viz_sec_button_left, 20 + 150, self.button_width, self.button_height), 'state': False, 'visible': False},
            {'text': 'Toggle Policy Arrows', 'rect': pygame.Rect(
                self.viz_sec_button_left, 20 + 200, self.button_width, self.button_height), 'state': False, 'visible': False},
        ]

        self.viz_sec_right_edge = self.viz_sec_left + self.button_width + 40
        self.viz_sec_bottom_edge = 20 + len(self.viz_config_buttons) * 50 + self.button_height + 20

        # Algorithm control section
        self.evaluation_steps = 0
        self.iteration_steps = 0

        self.is_eval_converged = False
        self.is_policy_converged = False

        self.cont_sec_left = self.viz_sec_left
        self.cont_sec_top = self.viz_sec_bottom_edge
        self.cont_sec_button_left = self.cont_sec_left + 20

        self.cont_sec_title = {'text': 'Algorithm Control', 'rect': pygame.Rect(
            self.cont_sec_button_left, self.cont_sec_top + 20, self.button_width, self.button_height)}

        # # of steps
        self.eval_step_counter = {'text': f'Evaluation Steps: {self.evaluation_steps}', 'rect': pygame.Rect(
            self.cont_sec_button_left, self.cont_sec_top + 20 + 50, self.button_width, self.button_height)}
        self.iter_step_counter = {'text': f'Iteration Steps: {self.iteration_steps}', 'rect': pygame.Rect(
            self.cont_sec_button_left, self.cont_sec_top + 20 + 150, self.button_width, self.button_height)}

        # algorithm control buttons
        self.algo_control_buttons = [
            {'text': 'Policy Evaluation', 'rect': pygame.Rect(
                self.cont_sec_button_left, self.cont_sec_top + 20 + 100, self.button_width, self.button_height), 'visible': False},
            {'text': 'Policy Improvement', 'rect': pygame.Rect(
                self.cont_sec_button_left, self.cont_sec_top + 20 + 200, self.button_width, self.button_height), 'visible': False},
            {'text': 'Reset Algorithm', 'rect': pygame.Rect(
                self.cont_sec_button_left, self.cont_sec_top + 20 + 250, self.button_width, self.button_height), 'visible': False},

            # For Value Iteration
            {'text': 'Iterate one step', 'rect': pygame.Rect(
                self.cont_sec_button_left, self.cont_sec_top + 20 + 200, self.button_width, self.button_height), 'visible': False},

            # For Model-Free algorithms
            {'text': 'Generate Experience', 'rect': pygame.Rect(
                self.cont_sec_button_left, self.cont_sec_top + 20 + 300, self.button_width, self.button_height), 'visible': False},
        ]

        self.cont_sec_bottom_edge = self.cont_sec_top + 20 + 300 + self.button_height + 20

        # Agent control section
        self.selected_action = None

        self.agent_sec_left = self.cont_sec_left
        self.agent_sec_top = self.cont_sec_bottom_edge
        self.agent_sec_button_left = self.agent_sec_left + 20

        self.agent_sec_title = {'text': 'Agent Control', 'rect': pygame.Rect(
            self.agent_sec_button_left, self.agent_sec_top + 20, self.button_width, self.button_height)}

        self.agent_control_buttons = [
            {'text': 'Move Agent', 'rect': pygame.Rect(
                self.agent_sec_button_left, self.agent_sec_top + 20 + 50, self.button_width, self.button_height), 'visible': True},
            {'text': 'Reset Agent', 'rect': pygame.Rect(
                self.agent_sec_button_left, self.agent_sec_top + 20 + 100, self.button_width, self.button_height), 'visible': True},
        ]

        # Screen
        self.WINDOW_SIZE = (self.viz_sec_right_edge, env.size * self.CELL_SIZE)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("GridWorld Visualization")

    def run(self):
        """Main visualization loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.handle_click(pos)

            self.screen.fill(self.WHITE)
            self.draw_grid()
            self.draw_agent()
            self.draw_algo_sec()
            self.draw_viz_sec()
            self.draw_algo_cont_sec()
            self.draw_agent_sec()
            pygame.display.flip()

        pygame.quit()

    def draw_grid(self):
        """Draw the grid and current state values."""
        for i in range(self.env.size):
            for j in range(self.env.size):
                rect = pygame.Rect(j * self.CELL_SIZE, i * self.CELL_SIZE,
                                   self.CELL_SIZE, self.CELL_SIZE)

                s = self.env.index_to_state(i, j)
                self.draw_cell_background(rect, s)
                self.draw_rewards(rect, s)
                self.draw_state_values(rect, s)
                self.draw_action_values(rect, s)
                self.draw_policy_arrows(rect, s)

    def draw_cell_background(self, rect, s):
        """Draw the background of a cell."""
        if s in self.env.terminal_states:
            color = self.GREEN if self.env.rewards[s] > 0 else self.RED
        elif s in self.env.walls:
            color = self.GRAY
        elif s in self.env.penalty_states:
            color = self.RED
        else:
            color = self.WHITE
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, self.BLACK, rect, 1)

    def draw_rewards(self, rect, s):
        """Draw rewards in a cell if enabled."""
        if self.show_rewards:
            text = self.font.render(f'{self.env.rewards[s]:.1f}', True, self.BLACK)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def draw_state_values(self, rect, s):
        """Draw state values in a cell if enabled."""
        if self.current_alg is not None and self.show_state_values:
            v_s = self.current_alg.values[s]
            text = self.font.render(f'{v_s:.2f}', True, self.BLACK)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def draw_action_values(self, rect, s):
        """Draw action values in a cell if enabled."""
        if self.current_alg is not None and self.show_action_values:
            for a in self.env.actions:
                q_sa = self.current_alg.q_values[s, a]
                text = self.font.render(f'{q_sa:.2f}', True, self.BLACK)
                if a == 0:
                    text_rect = text.get_rect(midtop=rect.midtop)
                elif a == 1:
                    text_rect = text.get_rect(midright=rect.midright)
                elif a == 2:
                    text_rect = text.get_rect(midbottom=rect.midbottom)
                elif a == 3:
                    text_rect = text.get_rect(midleft=rect.midleft)
                self.screen.blit(text, text_rect)

    def draw_policy_arrows(self, rect, s):
        """Draw policy arrows in a cell if enabled."""
        if self.current_alg is not None and self.show_policy:
            policy_probs = self.current_alg.policy[s]
            for a, prob in enumerate(policy_probs):
                if prob > 0:
                    start_pos, end_pos = self.get_arrow_positions(rect, a)
                    color = self.RED if s == self.env.agent_trace[-2] and a == self.selected_action else self.BLACK
                    self.draw_arrow(a, start_pos, end_pos, color)

    def get_arrow_positions(self, rect, a):
        """Get start and end positions for drawing an arrow."""
        if a == 0:  # Up
            start_pos = (rect.centerx, rect.centery - self.CELL_SIZE // 4)
            end_pos = (rect.centerx, rect.centery - self.CELL_SIZE // 2)
        elif a == 1:  # Right
            start_pos = (rect.centerx + self.CELL_SIZE // 4, rect.centery)
            end_pos = (rect.centerx + self.CELL_SIZE // 2, rect.centery)
        elif a == 2:  # Down
            start_pos = (rect.centerx, rect.centery + self.CELL_SIZE // 4)
            end_pos = (rect.centerx, rect.centery + self.CELL_SIZE // 2)
        elif a == 3:  # Left
            start_pos = (rect.centerx - self.CELL_SIZE // 4, rect.centery)
            end_pos = (rect.centerx - self.CELL_SIZE // 2, rect.centery)
        return start_pos, end_pos

    def draw_arrow(self, direction, start_pos, end_pos, color, width=2):
        """Draw an arrow from start_pos to end_pos."""
        pygame.draw.line(self.screen, color, start_pos, end_pos, width)
        if direction == 0:
            pygame.draw.polygon(self.screen, color, [(end_pos[0] - 5, end_pos[1] + 5),
                                                     end_pos,
                                                     (end_pos[0] + 5, end_pos[1] + 5)])
        elif direction == 1:
            pygame.draw.polygon(self.screen, color, [(end_pos[0] - 5, end_pos[1] - 5),
                                                     end_pos,
                                                     (end_pos[0] - 5, end_pos[1] + 5)])
        elif direction == 2:
            pygame.draw.polygon(self.screen, color, [(end_pos[0] - 5, end_pos[1] - 5),
                                                     end_pos,
                                                     (end_pos[0] + 5, end_pos[1] - 5)])
        elif direction == 3:
            pygame.draw.polygon(self.screen, color, [(end_pos[0] + 5, end_pos[1] - 5),
                                                     end_pos,
                                                     (end_pos[0] + 5, end_pos[1] + 5)])

    def draw_agent(self):
        """Draw the agent on the grid."""
        agent_pos = self.env.state_to_index(self.env.agent_state)
        agent_center = (agent_pos[1] * self.CELL_SIZE + self.CELL_SIZE // 2,
                        agent_pos[0] * self.CELL_SIZE + self.CELL_SIZE // 2)
        pygame.draw.circle(self.screen, self.BLUE, agent_center, self.agent_radius)

    def draw_algo_sec(self):
        """Draw algorithm selection section."""
        pygame.draw.rect(self.screen, self.WHITE, self.algo_sec_title['rect'])
        text = self.font.render(self.algo_sec_title['text'], True, self.BLACK)
        text_rect = text.get_rect(center=self.algo_sec_title['rect'].center)
        self.screen.blit(text, text_rect)
        # Draw left edge
        pygame.draw.line(self.screen, self.BLACK, (self.algo_sec_left_edge, 0),
                         (self.algo_sec_left_edge, self.WINDOW_SIZE[1]), 2)

        # current_algo color: GREEN
        # other algos color: WHITE
        for i, button in enumerate(self.algo_buttons):
            if self.current_alg is not None and button['text'] == f'{self.current_alg}':
                color = self.GREEN
            else:
                color = self.WHITE
            pygame.draw.rect(self.screen, color, button['rect'])
            pygame.draw.rect(self.screen, self.BLACK, button['rect'], 1)
            text = self.font.render(button['text'], True, self.BLACK)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

    def draw_viz_sec(self):
        """Draw visualization configuration section."""
        # Draw left edge
        pygame.draw.line(self.screen, self.BLACK, (self.viz_sec_left_edge, 0),
                         (self.viz_sec_left_edge, self.WINDOW_SIZE[1]), 2)

        # Draw title
        pygame.draw.rect(self.screen, self.WHITE, self.viz_sec_title['rect'])
        text = self.font.render(self.viz_sec_title['text'], True, self.BLACK)
        text_rect = text.get_rect(center=self.viz_sec_title['rect'].center)
        self.screen.blit(text, text_rect)

        for i, button in enumerate(self.viz_config_buttons):
            # Only draw reward button unless an algorithm is selected
            if i > 0 and self.current_alg is None:
                break

            # Toggle buttons color: GREEN if enabled, WHITE if disabled
            color = self.GREEN if button['state'] else self.WHITE
            pygame.draw.rect(self.screen, color, button['rect'])
            pygame.draw.rect(self.screen, self.BLACK, button['rect'], 1)
            text = self.font.render(button['text'], True, self.BLACK)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

        # Draw right edge
        pygame.draw.line(self.screen, self.BLACK, (self.viz_sec_right_edge, 0),
                         (self.viz_sec_right_edge, self.WINDOW_SIZE[1]), 2)
        # Draw bottom edge
        pygame.draw.line(self.screen, self.BLACK, (self.viz_sec_left, self.viz_sec_bottom_edge),
                         (self.viz_sec_right_edge, self.viz_sec_bottom_edge), 2)

    def draw_algo_cont_sec(self):
        """Draw algorithm control section."""
        # Draw title
        pygame.draw.rect(self.screen, self.WHITE, self.cont_sec_title['rect'])
        text = self.font.render(self.cont_sec_title['text'], True, self.BLACK)
        text_rect = text.get_rect(center=self.cont_sec_title['rect'].center)
        self.screen.blit(text, text_rect)

        # Draw steps and buttons w.r.t. current algorithm
        if isinstance(self.current_alg, PolicyIteration):
            self._draw_policy_iteration_controls()
        elif isinstance(self.current_alg, ValueIteration):
            self._draw_value_iteration_controls()
        else:
            # Draw nothing if no algorithm is selected
            pass

        # Draw bottom edge
        pygame.draw.line(self.screen, self.BLACK, (self.cont_sec_left, self.cont_sec_bottom_edge),
                         (self.viz_sec_right_edge, self.cont_sec_bottom_edge), 2)

    def _draw_policy_iteration_controls(self):
        # Draw steps
        self.eval_step_counter['text'] = f'Evaluation Steps: {self.evaluation_steps}'
        text = self.font.render(self.eval_step_counter['text'], True, self.BLACK)
        text_rect = text.get_rect(center=self.eval_step_counter['rect'].center)
        self.screen.blit(text, text_rect)

        self.iter_step_counter['text'] = f'Iteration Steps: {self.iteration_steps}'
        text = self.font.render(self.iter_step_counter['text'], True, self.BLACK)
        text_rect = text.get_rect(center=self.iter_step_counter['rect'].center)
        self.screen.blit(text, text_rect)

        # Draw buttons
        for i, button in enumerate(self.algo_control_buttons):
            if i > 2:
                button['visible'] = False
            else:
                button['visible'] = True
                pygame.draw.rect(self.screen, self.WHITE, button['rect'])
                pygame.draw.rect(self.screen, self.BLACK, button['rect'], 1)
                text = self.font.render(button['text'], True, self.BLACK)
                text_rect = text.get_rect(center=button['rect'].center)
                self.screen.blit(text, text_rect)

    def _draw_value_iteration_controls(self):
        # Draw steps
        self.iter_step_counter['text'] = f'Iteration Steps: {self.iteration_steps}'
        text = self.font.render(self.iter_step_counter['text'], True, self.BLACK)
        text_rect = text.get_rect(center=self.iter_step_counter['rect'].center)
        self.screen.blit(text, text_rect)

        # Draw buttons
        for i, button in enumerate(self.algo_control_buttons):
            if i < 2 or i > 3:
                button['visible'] = False
            else:
                button['visible'] = True

                pygame.draw.rect(self.screen, self.WHITE, button['rect'])
                pygame.draw.rect(self.screen, self.BLACK, button['rect'], 1)
                text = self.font.render(button['text'], True, self.BLACK)
                text_rect = text.get_rect(center=button['rect'].center)
                self.screen.blit(text, text_rect)

    def draw_agent_sec(self):
        """Draw agent control section."""
        # Draw title
        pygame.draw.rect(self.screen, self.WHITE, self.agent_sec_title['rect'])
        text = self.font.render(self.agent_sec_title['text'], True, self.BLACK)
        text_rect = text.get_rect(center=self.agent_sec_title['rect'].center)
        self.screen.blit(text, text_rect)

        # Draw buttons
        for i, button in enumerate(self.agent_control_buttons):
            pygame.draw.rect(self.screen, self.WHITE, button['rect'])
            pygame.draw.rect(self.screen, self.BLACK, button['rect'], 1)
            text = self.font.render(button['text'], True, self.BLACK)
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

    def handle_click(self, pos):
        """Handle mouse clicks on buttons."""
        # Algorithm selection buttons
        self.handle_algo_selection(pos)

        # Visualization configuration buttons
        self.handle_viz_config(pos)

        # Algorithm control buttons
        self.handle_algo_control(pos)

        # Agent control buttons
        self.handle_agent_control(pos)

    def handle_algo_selection(self, pos):
        """Handle algorithm selection button clicks."""
        for i, button in enumerate(self.algo_buttons):
            if button['rect'].collidepoint(pos):
                self.current_alg = self.algorithms[i]

    def handle_viz_config(self, pos):
        """Handle visualization configuration button clicks."""
        for i, button in enumerate(self.viz_config_buttons):
            if button['rect'].collidepoint(pos):
                button['state'] = not button['state']
                if button['text'] == 'Toggle Rewards':
                    self.show_rewards = button['state']
                elif button['text'] == 'Toggle State Values':
                    self.show_state_values = button['state']
                elif button['text'] == 'Toggle Action Values':
                    self.show_action_values = button['state']
                elif button['text'] == 'Toggle Policy Arrows':
                    self.show_policy = button['state']

    def handle_algo_control(self, pos):
        """Handle algorithm control button clicks."""
        for i, button in enumerate(self.algo_control_buttons):
            if not button['visible']:
                continue

            if button['rect'].collidepoint(pos):
                if self.current_alg is None:
                    self.show_toast("Please select an algorithm first!")
                else:
                    if button['text'] == 'Policy Evaluation':
                        self.policy_evaluation()
                    elif button['text'] == 'Policy Improvement':
                        self.policy_improvement()
                    elif button['text'] == 'Reset Algorithm':
                        self.reset_algorithm()
                    elif button['text'] == 'Iterate one step':
                        self.algo_step()

    def handle_agent_control(self, pos):
        """Handle agent control button clicks."""
        for i, button in enumerate(self.agent_control_buttons):
            if button['rect'].collidepoint(pos):
                if self.current_alg is None:
                    self.show_toast("Please select an algorithm first!")
                else:
                    if button['text'] == 'Move Agent':
                        self.move_agent()
                    elif button['text'] == 'Reset Agent':
                        self.reset_agent()

    def policy_evaluation(self):
        """Perform a policy evaluation step."""
        if self.is_eval_converged:
            self.show_toast("Policy evaluation already converged!")
        else:
            delta = self.current_alg.policy_evaluation_step()
            self.evaluation_steps += 1
            self.is_policy_converged = False

            if delta < 1e-6:
                self.show_toast("Policy evaluation converged!")
                self.is_eval_converged = True

    def policy_improvement(self):
        """Perform a policy improvement step."""
        if self.evaluation_steps == 0:
            self.show_toast("Please perform policy evaluation first!")
        elif self.is_policy_converged:
            self.show_toast("Policy improvement already converged!")
        else:
            is_policy_converged = self.current_alg.policy_improvement_step()
            self.evaluation_steps = 0
            self.is_eval_converged = False

            if is_policy_converged:
                self.show_toast("Policy improvement converged!")
                self.is_policy_converged = True

            self.iteration_steps += 1

    def reset_algorithm(self):
        """Reset the current algorithm."""
        self.current_alg.reset()
        self.evaluation_steps = 0
        self.iteration_steps = 0
        self.is_eval_converged = False
        self.is_policy_converged = False

    def algo_step(self):
        """Perform a single step of the algorithm."""
        if self.is_policy_converged:
            self.show_toast("Policy improvement already converged!")
        else:
            is_converged = self.current_alg.step()
            self.iteration_steps += 1

            if is_converged:
                self.show_toast("Algorithm converged!")
                self.is_policy_converged = True

    def move_agent(self):
        """Move the agent based on the current policy."""
        if self.env.is_terminated():
            self.show_toast("Agent already reached terminal state!")
        else:
            self.selected_action = self.current_alg.select_action(self.env.agent_state)
            done = self.current_alg.move_agent(self.selected_action)
            if done:
                self.show_toast("Agent reached terminal state!")

    def reset_agent(self):
        """Reset the agent to the initial state."""
        self.current_alg.reset_agent()

    def show_toast(self, message, duration=1000):
        """Show a toast message on the screen."""
        toast_font = pygame.font.Font(None, 36)
        toast_text = toast_font.render(message, True, self.RED)
        toast_rect = toast_text.get_rect(center=(self.WINDOW_SIZE[0] // 2, self.WINDOW_SIZE[1] // 2))

        # Draw white background for the toast
        background_rect = pygame.Rect(toast_rect.left - 10, toast_rect.top - 10,
                                      toast_rect.width + 20, toast_rect.height + 20)
        pygame.draw.rect(self.screen, self.WHITE, background_rect)

        self.screen.blit(toast_text, toast_rect)
        pygame.display.flip()
        pygame.time.delay(duration)
