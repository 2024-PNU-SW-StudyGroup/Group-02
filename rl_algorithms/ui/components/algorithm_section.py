# ui/components/algorithm_section.py
import pygame

class AlgorithmSection:
    def __init__(self, viz, left, top, width, height, algorithms, font, colors):
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
        for i, button in enumerate(self.algo_buttons):
            if button['rect'].collidepoint(pos):
                self.current_alg = self.algorithms[i]
                # 옵저버 통지
                self.viz.notify_observers('algorithm_changed', {
                    'algorithm': self.current_alg
                })

    def set_current_algorithm(self, alg):
        self.current_alg = alg