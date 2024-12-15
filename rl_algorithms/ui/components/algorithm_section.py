# ui/components/algorithm_section.py
import pygame

class AlgorithmSection:
    """
    Represents the algorithm selection section in the GridWorld visualization.

    This section allows the user to select an algorithm from a list of available
    algorithms. The selection is displayed visually and notifies observers about
    changes.

    Parameters
    ----------
    viz : GridWorldViz
        The visualization instance that manages this section.
    left : int
        The x-coordinate for the left edge of the section.
    top : int
        The y-coordinate for the top edge of the section.
    width : int
        The width of the section.
    height : int
        The height of the section.
    algorithms : list of str
        The list of algorithm names to be displayed.
    font : pygame.font.Font
        The font used for rendering text.
    colors : dict
        A dictionary containing color definitions.

    Attributes
    ----------
    viz : GridWorldViz
        The visualization instance managing this section.
    left : int
        The x-coordinate for the left edge of the section.
    top : int
        The y-coordinate for the top edge of the section.
    width : int
        The width of the section.
    height : int
        The height of the section.
    font : pygame.font.Font
        The font used for rendering text.
    BLACK : tuple
        The color black in RGB format.
    WHITE : tuple
        The color white in RGB format.
    GREEN : tuple
        The color green in RGB format.
    algorithms : list of str
        The list of algorithm names to be displayed.
    current_alg : str or None
        The currently selected algorithm.
    algo_sec_title : dict
        The title of the section and its rectangle properties.
    algo_buttons : list of dict
        The buttons for selecting algorithms, each with text and rectangle properties.

    Methods
    -------
    draw(screen, window_size)
        Draw the algorithm selection section on the screen.
    handle_click(pos)
        Handle mouse click events to select an algorithm.
    set_current_algorithm(alg)
        Update the currently selected algorithm.
    """

    def __init__(self, viz, left, top, width, height, algorithms, font, colors):
        """
        Initialize the AlgorithmSection.

        Parameters
        ----------
        viz : GridWorldViz
            The visualization instance managing this section.
        left : int
            The x-coordinate for the left edge of the section.
        top : int
            The y-coordinate for the top edge of the section.
        width : int
            The width of the section.
        height : int
            The height of the section.
        algorithms : list of str
            The list of algorithm names to be displayed.
        font : pygame.font.Font
            The font used for rendering text.
        colors : dict
            A dictionary containing color definitions.
        """
        self.viz = viz
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.font = font
        self.BLACK = colors['BLACK']
        self.WHITE = colors['WHITE']
        self.GREEN = colors['GREEN']

        self.algorithms = algorithms
        self.current_alg = None

        self.algo_sec_title = {
            'text': 'Select Algorithm',
            'rect': pygame.Rect(left+20, top+20, width, 40)
        }

        self.algo_buttons = []
        for i, algo in enumerate(algorithms):
            rect = pygame.Rect(left+20, top+(i+2)*50, width, 40)
            self.algo_buttons.append({'text': f'{algo}', 'rect': rect})

    def draw(self, screen, window_size):
        """
        Draw the algorithm selection section on the screen.

        Parameters
        ----------
        screen : pygame.Surface
            The surface to draw the section on.
        window_size : tuple of int
            The size of the window (width, height).
        """
        # Title
        pygame.draw.rect(screen, self.WHITE, self.algo_sec_title['rect'])
        text = self.font.render(self.algo_sec_title['text'], True, self.BLACK)
        text_rect = text.get_rect(center=self.algo_sec_title['rect'].center)
        screen.blit(text, text_rect)

        # Left edge line
        pygame.draw.line(screen, self.BLACK, (self.left, 0),
                         (self.left, window_size[1]), 2)

        # Buttons
        for button in self.algo_buttons:
            color = self.GREEN if (self.current_alg is not None and button['text'] == f'{self.current_alg}') else self.WHITE
            pygame.draw.rect(screen, color, button['rect'])
            pygame.draw.rect(screen, self.BLACK, button['rect'], 1)
            text = self.font.render(button['text'], True, self.BLACK)
            text_rect = text.get_rect(center=button['rect'].center)
            screen.blit(text, text_rect)

    def handle_click(self, pos):
        """
        Handle mouse click events to select an algorithm.

        Parameters
        ----------
        pos : tuple of int
            The (x, y) coordinates of the mouse click.
        """
        for i, button in enumerate(self.algo_buttons):
            if button['rect'].collidepoint(pos):
                self.current_alg = self.algorithms[i]
                # Notify observers
                self.viz.notify_observers('algorithm_changed', {
                    'algorithm': self.current_alg
                })

    def set_current_algorithm(self, alg):
        """
        Update the currently selected algorithm.

        Parameters
        ----------
        alg : str
            The algorithm to set as the current one.
        """
        self.current_alg = alg