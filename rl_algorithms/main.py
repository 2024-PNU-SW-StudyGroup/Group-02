# main.py
import os
import sys
import numpy as np

# 프로젝트 루트 디렉토리를 Python 경로에 추가
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, BASE_DIR)

# 프로젝트 구조에 맞추어 import
from core.rl_env.grid_world import GridWorld
from core.algorithms.policy_iteration import PolicyIteration
from core.algorithms.value_iteration import ValueIteration
from ui.grid_world_viz import GridWorldViz
from ui.observers.ui_update_observer import UIUpdateObserver
# 필요하다면 QLearning도 여기서 import
# from core.algorithms.q_learning import QLearning

def main(seed=42):
    # 환경 생성
    env = GridWorld(size=7, seed=seed)

    # 알고리즘 인스턴스 생성
    algorithms = [
        PolicyIteration(env, gamma=0.9, seed=seed),
        ValueIteration(env, gamma=0.9, seed=seed),
        # QLearning(env, gamma=0.9, alpha=0.1, epsilon=0.1, seed=seed) # 필요시 추가
    ]

    # 시각화 인스턴스 생성
    viz = GridWorldViz(env, algorithms)

    # 옵저버 생성 및 등록
    ui_observer = UIUpdateObserver(viz)
    viz.add_observer(ui_observer)

    # 시각화 실행
    viz.run()

if __name__ == "__main__":
    np.random.seed(42)
    main(seed=42)