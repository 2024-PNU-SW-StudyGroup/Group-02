# ui/components/visualization_section.py
import pygame

class VisualizationSection:
    def __init__(self, viz, left, top, width, font, colors):
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
        return {
            'show_rewards': self.show_rewards,
            'show_state_values': self.show_state_values,
            'show_action_values': self.show_action_values,
            'show_policy': self.show_policy
        }