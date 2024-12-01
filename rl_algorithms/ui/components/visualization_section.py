import pygame

class VisualizationSection:
    def __init__(self, screen, button_width=280, button_height=40, left_offset=20, top_offset=20):
        self.screen = screen
        self.button_width = button_width
        self.button_height = button_height
        self.left = left_offset
        self.top = top_offset
        self.font = pygame.font.Font(None, 24)

        self.title = {'text': 'Toggle Visualization', 'rect': pygame.Rect(
            self.left, self.top, self.button_width, self.button_height)}
        self.buttons = [
            {'text': 'Toggle Rewards', 'rect': pygame.Rect(
                self.left, self.top + 50, self.button_width, self.button_height), 'state': True},
            {'text': 'Toggle State Values', 'rect': pygame.Rect(
                self.left, self.top + 100, self.button_width, self.button_height), 'state': False},
            {'text': 'Toggle Action Values', 'rect': pygame.Rect(
                self.left, self.top + 150, self.button_width, self.button_height), 'state': False},
            {'text': 'Toggle Policy Arrows', 'rect': pygame.Rect(
                self.left, self.top + 200, self.button_width, self.button_height), 'state': False},
        ]

    def draw(self, show_rewards, show_state_values, show_action_values, show_policy):
        pygame.draw.rect(self.screen, (255, 255, 255), self.title['rect'])
        pygame.draw.rect(self.screen, (0, 0, 0), self.title['rect'], 1)
        text = self.font.render(self.title['text'], True, (0, 0, 0))
        text_rect = text.get_rect(center=self.title['rect'].center)
        self.screen.blit(text, text_rect)

        states = [show_rewards, show_state_values, show_action_values, show_policy]
        for i, button in enumerate(self.buttons):
            color = (0, 255, 0) if states[i] else (255, 255, 255)
            pygame.draw.rect(self.screen, color, button['rect'])
            pygame.draw.rect(self.screen, (0, 0, 0), button['rect'], 1)
            text = self.font.render(button['text'], True, (0, 0, 0))
            text_rect = text.get_rect(center=button['rect'].center)
            self.screen.blit(text, text_rect)

    def handle_click(self, pos, current_state):
        for i, button in enumerate(self.buttons):
            if button['rect'].collidepoint(pos):
                button['state'] = not button['state']
                current_state[i] = button['state']
                return {'type': button['text'], 'state': button['state']}
        return None

    def update_visualization(self, viz_type, state):
        for button in self.buttons:
            if button['text'] == viz_type:
                button['state'] = state
        self.draw(buttons_state= [btn['state'] for btn in self.buttons])