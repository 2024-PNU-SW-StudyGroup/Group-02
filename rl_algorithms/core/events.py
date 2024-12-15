# src/core/events.py

from enum import Enum

class EventType(Enum):
    AGENT_MOVED = 'agent_moved'
    POLICY_EVALUATION = 'policy_evaluation'
    ALGORITHM_CHANGED = 'algorithm_changed'
    VISUALIZATION_CHANGED = 'visualization_changed'
    # 기타 이벤트 타입 정의
