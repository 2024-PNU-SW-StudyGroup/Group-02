# ui/grid_world_viz.py
import pygame
from rl_algorithms.ui.observers.base_observer import UIObserver
from rl_algorithms.ui.observers.ui_update_observer import UIUpdateObserver
from rl_algorithms.ui.components.algorithm_section import AlgorithmSection
from rl_algorithms.ui.components.visualization_section import VisualizationSection
from rl_algorithms.ui.components.control_section import ControlSection
from rl_algorithms.ui.components.grid import GridComponent

class GridWorldViz:
    """
    Visualization manager for the GridWorld environment.

    Attributes
    ----------
    env : object
        The environment object representing the GridWorld.
    algorithms : list
        List of RL algorithms used in the visualization.
    colors : dict
        Color codes for various UI elements.
    font : pygame.font.Font
        Font used for rendering text.
    CELL_SIZE : int
        Size of each cell in the grid.
    WINDOW_SIZE : tuple
        Dimensions of the visualization window.
    screen : pygame.Surface
        The main display surface.
    observers : list
        List of observer objects for event handling.
    algorithm_section : AlgorithmSection
        Component for managing algorithm-related UI elements.
    visualization_section : VisualizationSection
        Component for managing visualization toggle options.
    control_section : ControlSection
        Component for managing control-related UI elements.
    grid : GridComponent
        Component for rendering the GridWorld grid.
    current_alg : object
        Currently selected algorithm for visualization.

    Methods
    -------
    add_observer(observer)
        Add an observer for event notifications.
    remove_observer(observer)
        Remove an observer from event notifications.
    notify_observers(event_type, data=None)
        Notify all observers of a specific event.
    run()
        Start the visualization loop.
    draw_all()
        Render all components in the visualization.
    handle_click(pos)
        Handle mouse click events and delegate to components.
    show_toast(message, duration=1000)
        Display a temporary message on the screen.
    """
    def __init__(self, env, algorithms):
        """
        Initialize the GridWorldViz with environment and algorithms.

        Parameters
        ----------
        env : object
            The GridWorld environment to visualize.
        algorithms : list
            List of RL algorithms to support in the visualization.
        """
        pygame.init()

        self.env = env
        self.algorithms = algorithms

        # Colors
        self.colors = {
            'WHITE': (255, 255, 255),
            'BLACK': (0, 0, 0),
            'GRAY': (128, 128, 128),
            'RED': (255, 0, 0),
            'GREEN': (0, 255, 0),
            'BLUE': (0, 0, 255)
        }

        # Font & Cell size
        self.font = pygame.font.Font(None, 24)
        self.CELL_SIZE = 125

        # Window calculation
        self.algo_sec_left = env.size * self.CELL_SIZE
        self.viz_sec_left = self.algo_sec_left + 20 + 280 + 20
        self.viz_sec_right_edge = self.viz_sec_left + 280 + 40

        self.WINDOW_SIZE = (self.viz_sec_right_edge, env.size * self.CELL_SIZE)
        self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
        pygame.display.set_caption("GridWorld Visualization")

        # Observer list
        self.observers = []
        self.add_observer(UIUpdateObserver(self))

        # Components 초기화 (algorithm_section를 먼저 초기화)
        self.algorithm_section = AlgorithmSection(
            viz=self,
            left=self.algo_sec_left,
            top=0,
            width=280,
            height=40,
            algorithms=self.algorithms,
            font=self.font,
            colors=self.colors
        )

        self.visualization_section = VisualizationSection(
            viz=self,
            left=self.viz_sec_left,
            top=0,
            width=280,
            font=self.font,
            colors=self.colors
        )

        viz_sec_bottom_edge = 20 + len(self.visualization_section.buttons)*50 + 40 + 20
        self.control_section = ControlSection(
            viz=self,
            left=self.viz_sec_left,
            top=viz_sec_bottom_edge,
            width=280,
            font=self.font,
            colors=self.colors
        )

        self.grid = GridComponent(
            viz=self,
            cell_size=self.CELL_SIZE,
            font=self.font,
            colors=self.colors
        )

        # 모든 컴포넌트 초기화 후 current_alg 설정
        self.current_alg = None  # 이 때 setter가 호출되어도 algorithm_section가 존재하므로 OK
    
    def add_observer(self, observer: UIObserver):
        """
        Add an observer to receive event notifications.

        Parameters
        ----------
        observer : UIObserver
            Observer to be added to the list.
        """
        self.observers.append(observer)

    def remove_observer(self, observer: UIObserver):
        """
        Remove an observer from receiving event notifications.

        Parameters
        ----------
        observer : UIObserver
            Observer to be removed from the list.
        """
        self.observers.remove(observer)

    def notify_observers(self, event_type: str, data: dict = None):
        """
        Notify all observers of a specific event.

        Parameters
        ----------
        event_type : str
            The type of event being notified.
        data : dict, optional
            Additional data related to the event (default is None).
        """
        for observer in self.observers:
            observer.update(event_type, data)

    def run(self):
        """
        Start the main loop for the visualization.
        """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.handle_click(pos)

            self.screen.fill(self.colors['WHITE'])
            self.draw_all()
            pygame.display.flip()

        pygame.quit()

    def draw_all(self):
        """
        Render all components in the visualization.
        """
        # Grid and Agent
        viz_states = self.visualization_section.get_states()
        self.grid.draw(self.screen, **viz_states, current_alg=self.current_alg)

        # Draw Sections
        self.algorithm_section.draw(self.screen, self.WINDOW_SIZE)
        self.visualization_section.draw(self.screen, self.WINDOW_SIZE, self.current_alg)
        self.control_section.draw(self.screen, self.WINDOW_SIZE, self.current_alg)

    def handle_click(self, pos):
        """
        Handle mouse click events and delegate to relevant components.

        Parameters
        ----------
        pos : tuple
            The position of the mouse click.
        """
        self.algorithm_section.handle_click(pos)
        self.visualization_section.handle_click(pos, self.current_alg)
        self.control_section.handle_click(pos, self.current_alg)

    def show_toast(self, message, duration=1000):
        """
        Display a temporary message on the screen.

        Parameters
        ----------
        message : str
            The message to be displayed.
        duration : int, optional
            Duration in milliseconds to display the message (default is 1000).
        """
        toast_font = pygame.font.Font(None, 36)
        toast_text = toast_font.render(message, True, self.colors['RED'])
        toast_rect = toast_text.get_rect(center=(self.WINDOW_SIZE[0] // 2, self.WINDOW_SIZE[1] // 2))

        background_rect = pygame.Rect(toast_rect.left - 10, toast_rect.top - 10,
                                      toast_rect.width + 20, toast_rect.height + 20)
        pygame.draw.rect(self.screen, self.colors['WHITE'], background_rect)

        self.screen.blit(toast_text, toast_rect)
        pygame.display.flip()
        pygame.time.delay(duration)

    @property
    def env(self):
        """
        Get the environment.

        Returns
        -------
        object
            The current environment.
        """
        return self._env

    @env.setter
    def env(self, environment):
        """
        Set the environment.

        Parameters
        ----------
        environment : object
            The new environment to be set.
        """
        self._env = environment

    @property
    def current_alg(self):
        """
        Get the currently selected algorithm.

        Returns
        -------
        object
            The currently selected algorithm.
        """
        return self._current_alg

    @current_alg.setter
    def current_alg(self, alg):
        """
        Set the currently selected algorithm.

        Parameters
        ----------
        alg : object
            The new algorithm to be selected.
        """
        self._current_alg = alg
        self.algorithm_section.set_current_algorithm(alg)