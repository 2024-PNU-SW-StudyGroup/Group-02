# ui/grid_world_viz.py
import pygame
from ui.observers.base_observer import UIObserver
from ui.observers.ui_update_observer import UIUpdateObserver
from ui.components.algorithm_section import AlgorithmSection
from ui.components.visualization_section import VisualizationSection
from ui.components.control_section import ControlSection
from ui.components.grid import GridComponent

class GridWorldViz:
    def __init__(self, env, algorithms):
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
        self.observers.append(observer)

    def remove_observer(self, observer: UIObserver):
        self.observers.remove(observer)

    def notify_observers(self, event_type: str, data: dict = None):
        for observer in self.observers:
            observer.update(event_type, data)

    def run(self):
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
        # Grid and Agent
        viz_states = self.visualization_section.get_states()
        self.grid.draw(self.screen, **viz_states, current_alg=self.current_alg)

        # Draw Sections
        self.algorithm_section.draw(self.screen, self.WINDOW_SIZE)
        self.visualization_section.draw(self.screen, self.WINDOW_SIZE, self.current_alg)
        self.control_section.draw(self.screen, self.WINDOW_SIZE, self.current_alg)

    def handle_click(self, pos):
        self.algorithm_section.handle_click(pos)
        self.visualization_section.handle_click(pos, self.current_alg)
        self.control_section.handle_click(pos, self.current_alg)

    def show_toast(self, message, duration=1000):
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
        return self._env

    @env.setter
    def env(self, environment):
        self._env = environment

    @property
    def current_alg(self):
        return self._current_alg

    @current_alg.setter
    def current_alg(self, alg):
        self._current_alg = alg
        self.algorithm_section.set_current_algorithm(alg)