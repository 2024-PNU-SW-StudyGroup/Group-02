# src/ui/grid_world_viz.py

import pygame
from ui.components.grid import Grid
from ui.components.algorithm_section import AlgorithmSection
from ui.components.visualization_section import VisualizationSection
from ui.components.control_section import ControlSection
from ui.observers.ui_observer import UIUpdateObserver
from core.env.grid_world import GridWorld
from core.algorithms.policy_iteration import PolicyIteration
from core.algorithms.value_iteration import ValueIteration

class GridWorldViz:
    def __init__(self, env, algorithms):
        pygame.init()
        self.env = env
        self.algorithms = algorithms
        self.current_alg = None

        # 화면 설정
        self.CELL_SIZE = 125
        screen_width = env.size * self.CELL_SIZE + 300  # 추가 패널 공간
        screen_height = env.size * self.CELL_SIZE
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("GridWorld Visualization")

        # UI 컴포넌트 초기화
        self.grid = Grid(env, self.screen, self.CELL_SIZE)
        self.algorithm_section = AlgorithmSection(algorithms, self.screen)
        self.visualization_section = VisualizationSection(self.screen)
        self.control_section = ControlSection(self.screen)

        # 옵저버 초기화 및 등록
        self.observers = []
        self.ui_observer = UIUpdateObserver(self)
        self.add_observer(self.ui_observer)

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, event_type, data=None):
        for observer in self.observers:
            observer.update(event_type, data)

    def run(self):
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.handle_click(pos)

            self.screen.fill((200, 200, 200))  # 배경색

            # 그리드 그리기
            self.grid.draw(self.current_alg)

            # 알고리즘 섹션 그리기
            self.algorithm_section.draw(self.current_alg)

            # 시각화 섹션 그리기
            self.visualization_section.draw(
                self.visualization_section.show_rewards,
                self.visualization_section.show_state_values,
                self.visualization_section.show_action_values,
                self.visualization_section.show_policy
            )

            # 제어 섹션 그리기
            self.control_section.draw(
                self.env.is_eval_converged,
                self.env.is_policy_converged,
                self.env.evaluation_steps,
                self.env.iteration_steps
            )

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

    def handle_click(self, pos):
        # 알고리즘 선택 처리
        selected_alg = self.algorithm_section.handle_click(pos)
        if selected_alg:
            self.current_alg = selected_alg
            self.notify_observers('algorithm_changed', {'algorithm': self.current_alg})

        # 시각화 설정 처리
        viz_update = self.visualization_section.handle_click(pos, [
            self.visualization_section.show_rewards,
            self.visualization_section.show_state_values,
            self.visualization_section.show_action_values,
            self.visualization_section.show_policy
        ])
        if viz_update:
            self.notify_observers('visualization_changed', viz_update)

        # 알고리즘 제어 버튼 처리
        control_action = self.control_section.handle_click(pos)
        if control_action:
            self.perform_control_action(control_action)

        # 에이전트 제어 버튼 처리
        # 여기에 에이전트 제어 버튼 로직을 추가할 수 있습니다.

    def perform_control_action(self, action):
        if action == 'Policy Evaluation':
            if self.current_alg:
                converged = self.current_alg.policy_evaluation_step()
                self.env.evaluation_steps += 1
                if converged:
                    self.env.is_eval_converged = True
                self.notify_observers('policy_evaluation', {
                    'steps': self.env.evaluation_steps,
                    'delta': self.current_alg.delta,
                    'converged': converged
                })
        elif action == 'Policy Improvement':
            if self.current_alg:
                converged = self.current_alg.policy_improvement_step()
                if converged:
                    self.env.is_policy_converged = True
                self.notify_observers('policy_improvement', {
                    'converged': converged
                })
        elif action == 'Reset Algorithm':
            if self.current_alg:
                self.current_alg.reset()
                self.env.evaluation_steps = 0
                self.env.iteration_steps = 0
                self.env.is_eval_converged = False
                self.env.is_policy_converged = False
                self.notify_observers('reset_algorithm')
        elif action == 'Iterate one step':
            if self.current_alg:
                converged = self.current_alg.step()
                self.env.iteration_steps += 1
                if converged:
                    self.env.is_policy_converged = True
                self.notify_observers('algo_step', {
                    'converged': converged
                })
        elif action == 'Generate Experience':
            # Model-Free 알고리즘에 대한 경험 생성 로직을 여기에 추가할 수 있습니다.
            pass
