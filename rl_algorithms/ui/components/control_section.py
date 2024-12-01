import pygame

class ControlSection:
    def __init__(self, screen, button_width=280, button_height=40, left_offset=20, top_offset=20):
        self.screen = screen
        self.button_width = button_width
        self.button_height = button_height
        self.left = left_offset
        self.top = top_offset
        self.font = pygame.font.Font(None, 24)
        self.current_alg = None

        self.title = {'text': 'Algorithm Control', 'rect': pygame.Rect(
            self.left, self.top, self.button_width, self.button_height)}
        self.buttons = [
            {'text': 'Policy Evaluation', 'rect': pygame.Rect(
                self.left, self.top + 100, self.button_width, self.button_height), 'visible': False},
            {'text': 'Policy Improvement', 'rect': pygame.Rect(
                self.left, self.top + 200, self.button_width, self.button_height), 'visible': False},
            {'text': 'Reset Algorithm', 'rect': pygame.Rect(
                self.left, self.top + 250, self.button_width, self.button_height), 'visible': False},
            {'text': 'Iterate one step', 'rect': pygame.Rect(
                self.left, self.top + 200, self.button_width, self.button_height), 'visible': False},
            {'text': 'Generate Experience', 'rect': pygame.Rect(
                self.left, self.top + 300, self.button_width, self.button_height), 'visible': False},
        ]
        self.evaluation_steps = 0
        self.iteration_steps = 0

    def draw(self, is_eval_converged, is_policy_converged, eval_steps, iter_steps):
        pygame.draw.rect(self.screen, (255, 255, 255), self.title['rect'])
        pygame.draw.rect(self.screen, (0, 0, 0), self.title['rect'], 1)
        text = self.font.render(self.title['text'], True, (0, 0, 0))
        text_rect = text.get_rect(center=self.title['rect'].center)
        self.screen.blit(text, text_rect)

        # 단계 표시
        eval_text = self.font.render(f'Evaluation Steps: {eval_steps}', True, (0, 0, 0))
        eval_rect = eval_text.get_rect(center=(self.left + self.button_width // 2, self.top + 50))
        self.screen.blit(eval_text, eval_rect)

        iter_text = self.font.render(f'Iteration Steps: {iter_steps}', True, (0, 0, 0))
        iter_rect = iter_text.get_rect(center=(self.left + self.button_width // 2, self.top + 150))
        self.screen.blit(iter_text, iter_rect)

        # 버튼 표시
        for button in self.buttons:
            if not button['visible']:
                continue
            pygame.draw.rect(self.screen, (255, 255, 255), button['rect'])
            pygame.draw.rect(self.screen, (0, 0, 0), button['rect'], 1)
            text = self.font.render(button['text'], True, (0, 0, 0))
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

    def handle_click(self, pos):
        for button in self.buttons:
            if button['visible'] and button['rect'].collidepoint(pos):
                return button['text']
        return None

    def update_algorithm(self, algorithm):
        self.current_alg = algorithm
        if isinstance(algorithm, type):  # 알고리즘 클래스 타입
            if algorithm.__name__ == 'PolicyIteration':
                self.buttons[0]['visible'] = True
                self.buttons[1]['visible'] = True
                self.buttons[2]['visible'] = True
                self.buttons[3]['visible'] = False
                self.buttons[4]['visible'] = False
            elif algorithm.__name__ == 'ValueIteration':
                self.buttons[0]['visible'] = False
                self.buttons[1]['visible'] = False
                self.buttons[2]['visible'] = False
                self.buttons[3]['visible'] = True
                self.buttons[4]['visible'] = False
            # 추가 알고리즘에 대한 설정
        self.draw(None, None, self.evaluation_steps, self.iteration_steps)

    def update_evaluation(self, eval_data):
        self.evaluation_steps = eval_data['steps']
        if eval_data['converged']:
            # 정책 평가가 수렴했을 때 추가 로직
            pass
        self.draw(None, None, self.evaluation_steps, self.iteration_steps)

    def update_iteration(self, iter_steps):
        self.iteration_steps = iter_steps
        self.draw(None, None, self.evaluation_steps, self.iteration_steps)