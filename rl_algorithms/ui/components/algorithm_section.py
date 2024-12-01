import pygame

class AlgorithmSection:
    def __init__(self, algorithms, screen, button_width=280, button_height=40, left_offset=20, top_offset=20):
        self.algorithms = algorithms
        self.screen = screen
        self.button_width = button_width
        self.button_height = button_height
        self.left = left_offset
        self.top = top_offset
        self.font = pygame.font.Font(None, 24)
        self.current_alg = None

        self.title = {'text': 'Select Algorithm', 'rect': pygame.Rect(
            self.left, self.top, self.button_width, self.button_height)}
        self.buttons = [
            {'text': f'{algo.__class__.__name__}', 'rect': pygame.Rect(
                self.left, self.top + (i + 1) * 50, self.button_width, self.button_height)} for i, algo in enumerate(algorithms)
        ]

    def draw(self, current_alg):
        pygame.draw.rect(self.screen, (255, 255, 255), self.title['rect'])
        pygame.draw.rect(self.screen, (0, 0, 0), self.title['rect'], 1)
        text = self.font.render(self.title['text'], True, (0, 0, 0))
        text_rect = text.get_rect(center=self.title['rect'].center)
        self.screen.blit(text, text_rect)

        for i, button in enumerate(self.buttons):
            if current_alg and button['text'] == current_alg.__class__.__name__:
                color = (0, 255, 0)  # 현재 선택된 알고리즘은 녹색
            else:
                color = (255, 255, 255)  # 선택되지 않은 알고리즘은 흰색
            pygame.draw.rect(self.screen, color, button['rect'])
            pygame.draw.rect(self.screen, (0, 0, 0), button['rect'], 1)
            text = self.font.render(button['text'], True, (0, 0, 0))
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

    def handle_click(self, pos):
        for i, button in enumerate(self.buttons):
            if button['rect'].collidepoint(pos):
                return self.algorithms[i]
        return None

    def update_algorithm(self, algorithm):
        self.current_alg = algorithm
        self.draw(self.current_alg)