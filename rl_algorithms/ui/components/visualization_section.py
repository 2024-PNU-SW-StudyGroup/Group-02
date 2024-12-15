# ui/components/visualization_section.py
import pygame

class VisualizationSection:
    """
    Handles the visualization controls for toggling various display elements in the Grid World environment.

    Attributes
    ----------
    viz : object
        The visualization object containing the environment and observers.
    left : int
        The left margin of the section.
    top : int
        The top margin of the section.
    width : int
        The width of the section.
    font : pygame.font.Font
        The font used for rendering text.
    BLACK, WHITE, GREEN : tuple
        RGB color values for rendering UI components.
    title_rect : pygame.Rect
        The rectangle for the section title.
    buttons : list
        A list of dictionaries representing buttons and their states.
    show_rewards : bool
        Whether to display rewards in the visualization.
    show_state_values : bool
        Whether to display state values in the visualization.
    show_action_values : bool
        Whether to display action values in the visualization.
    show_policy : bool
        Whether to display policy arrows in the visualization.
    """
    def __init__(self, viz, left, top, width, font, colors):
        """
        Initializes the VisualizationSection.

        Parameters
        ----------
        viz : object
            The visualization object.
        left : int
            The left margin of the section.
        top : int
            The top margin of the section.
        width : int
            The width of the section.
        font : pygame.font.Font
            The font used for rendering text.
        colors : dict
            A dictionary of RGB color values for various UI components.
        """
        self.viz = viz
        self.left = left
        self.top = top
        self.width = width
        self.font = font
        self.BLACK = colors['BLACK']
        self.WHITE = colors['WHITE']
        self.GREEN = colors['GREEN']

        self.title_rect = pygame.Rect(left+20, top+20, width, 40)

        self.buttons = [
            {'text': 'Toggle Rewards', 'rect': pygame.Rect(left+20, top+70, width, 40), 'state': True, 'visible': True},
            {'text': 'Toggle State Values', 'rect': pygame.Rect(left+20, top+120, width, 40), 'state': False, 'visible': False},
            {'text': 'Toggle Action Values', 'rect': pygame.Rect(left+20, top+170, width, 40), 'state': False, 'visible': False},
            {'text': 'Toggle Policy Arrows', 'rect': pygame.Rect(left+20, top+220, width, 40), 'state': False, 'visible': False},
        ]

        self.show_rewards = True
        self.show_state_values = False
        self.show_action_values = False
        self.show_policy = False

    def draw(self, screen, window_size, current_alg):
        """
        Draws the visualization control section and its buttons.

        Parameters
        ----------
        screen : pygame.Surface
            The surface on which to draw.
        window_size : tuple
            The size of the window (width, height).
        current_alg : object
            The currently selected reinforcement learning algorithm.
        """
        # Left edge
        pygame.draw.line(screen, self.BLACK, (self.left, 0),
                         (self.left, window_size[1]), 2)
        # Title
        pygame.draw.rect(screen, self.WHITE, self.title_rect)
        text = self.font.render('Toggle Visualization', True, self.BLACK)
        text_rect = text.get_rect(center=self.title_rect.center)
        screen.blit(text, text_rect)

        for i, button in enumerate(self.buttons):
            if i > 0 and current_alg is None:
                break
            color = self.GREEN if button['state'] else self.WHITE
            pygame.draw.rect(screen, color, button['rect'])
            pygame.draw.rect(screen, self.BLACK, button['rect'], 1)
            text = self.font.render(button['text'], True, self.BLACK)
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)

    def handle_click(self, pos, current_alg):
        """
        Handles mouse click events to toggle visualization options.

        Parameters
        ----------
        pos : tuple
            The (x, y) position of the mouse click.
        current_alg : object
            The currently selected reinforcement learning algorithm.
        """
        for i, button in enumerate(self.buttons):
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
                
                self.viz.notify_observers('visualization_changed', {
                    'type': button['text'],
                    'state': button['state']
                })

    def get_states(self):
        """
        Retrieves the current visualization states.

        Returns
        -------
        dict
            A dictionary of the current visualization states.
        """
        return {
            'show_rewards': self.show_rewards,
            'show_state_values': self.show_state_values,
            'show_action_values': self.show_action_values,
            'show_policy': self.show_policy
        }
    
    def update_visualization(self, viz_type, state):
        """
        Updates the visualization states based on an observer event.

        Parameters
        ----------
        viz_type : str
            The type of visualization to update ('Toggle Rewards', 'Toggle State Values', etc.).
        state : bool
            The new state (True/False) for the visualization type.
        """
        if viz_type == 'Toggle Rewards':
            self.show_rewards = state
        elif viz_type == 'Toggle State Values':
            self.show_state_values = state
        elif viz_type == 'Toggle Action Values':
            self.show_action_values = state
        elif viz_type == 'Toggle Policy Arrows':
            self.show_policy = state
        # 필요한 경우 추가 UI 업데이트 로직 삽입