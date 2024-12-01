import pygame

class Grid:
    def __init__(self, env, screen, cell_size):
        self.env = env
        self.screen = screen
        self.cell_size = cell_size
        self.font = pygame.font.Font(None, 24)
        
        # 색상 정의
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (128, 128, 128)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        
        self.agent_radius = self.cell_size // 4

    def draw(self, current_alg):
        for i in range(self.env.size):
            for j in range(self.env.size):
                rect = pygame.Rect(j * self.cell_size, i * self.cell_size,
                                   self.cell_size, self.cell_size)
                s = self.env.index_to_state(i, j)
                self.draw_cell_background(rect, s)
                self.draw_rewards(rect, s)
                self.draw_state_values(rect, s, current_alg)
                self.draw_action_values(rect, s, current_alg)
                self.draw_policy_arrows(rect, s, current_alg)

    def draw_cell_background(self, rect, s):
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
        if self.env.show_rewards:
            text = self.font.render(f'{self.env.rewards[s]:.1f}', True, self.BLACK)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def draw_state_values(self, rect, s, current_alg):
        if current_alg and self.env.show_state_values:
            v_s = current_alg.values[s]
            text = self.font.render(f'{v_s:.2f}', True, self.BLACK)
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

    def draw_action_values(self, rect, s, current_alg):
        if current_alg and self.env.show_action_values:
            for a in self.env.actions:
                q_sa = current_alg.q_values[s, a]
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

    def draw_policy_arrows(self, rect, s, current_alg):
        if current_alg and self.env.show_policy:
            policy_probs = current_alg.policy[s]
            for a, prob in enumerate(policy_probs):
                if prob > 0:
                    start_pos, end_pos = self.get_arrow_positions(rect, a)
                    color = self.RED if s == self.env.agent_trace[-2] and a == self.env.selected_action else self.BLACK
                    self.draw_arrow(a, start_pos, end_pos, color)

    def get_arrow_positions(self, rect, a):
        if a == 0:  # Up
            start_pos = (rect.centerx, rect.centery - self.cell_size // 4)
            end_pos = (rect.centerx, rect.centery - self.cell_size // 2)
        elif a == 1:  # Right
            start_pos = (rect.centerx + self.cell_size // 4, rect.centery)
            end_pos = (rect.centerx + self.cell_size // 2, rect.centery)
        elif a == 2:  # Down
            start_pos = (rect.centerx, rect.centery + self.cell_size // 4)
            end_pos = (rect.centerx, rect.centery + self.cell_size // 2)
        elif a == 3:  # Left
            start_pos = (rect.centerx - self.cell_size // 4, rect.centery)
            end_pos = (rect.centerx - self.cell_size // 2, rect.centery)
        return start_pos, end_pos

    def draw_arrow(self, direction, start_pos, end_pos, color, width=2):
        pygame.draw.line(self.screen, color, start_pos, end_pos, width)
        if direction == 0:
            pygame.draw.polygon(self.screen, color, [
                (end_pos[0] - 5, end_pos[1] + 5),
                end_pos,
                (end_pos[0] + 5, end_pos[1] + 5)
            ])
        elif direction == 1:
            pygame.draw.polygon(self.screen, color, [
                (end_pos[0] - 5, end_pos[1] - 5),
                end_pos,
                (end_pos[0] - 5, end_pos[1] + 5)
            ])
        elif direction == 2:
            pygame.draw.polygon(self.screen, color, [
                (end_pos[0] - 5, end_pos[1] - 5),
                end_pos,
                (end_pos[0] + 5, end_pos[1] - 5)
            ])
        elif direction == 3:
            pygame.draw.polygon(self.screen, color, [
                (end_pos[0] + 5, end_pos[1] - 5),
                end_pos,
                (end_pos[0] + 5, end_pos[1] + 5)
            ])

    def update_agent(self, agent_data):
        # 에이전트의 상태가 변경되면 호출됩니다.
        # 필요시 추가적인 업데이트 로직을 구현할 수 있습니다.
        pass