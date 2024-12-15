# **Grid World Reinforcement Learning Visualizer**
<img width="1440" alt="example" src="https://github.com/user-attachments/assets/39075e0f-7fd1-4c74-9cc6-9e8a311a6edb" />

### **프로젝트 설명**
`Grid World Reinforcement Learning Visualizer`는 **강화학습(Reinforcement Learning)** 알고리즘을 실시간으로 시각화하여 학습자와 연구자가 알고리즘의 내부 동작을 이해할 수 있도록 돕는 교육용 도구입니다.  
이 도구는 Python과 `pygame`을 사용하여 제작되었으며, **Policy Iteration**, **Value Iteration** 등 다양한 RL 알고리즘의 상태값(Value), 행동(Action), 정책(Policy)을 시각적으로 표현합니다.

---

## **프로젝트 목표**
1. **강화학습 알고리즘 이해 증진:**
   - 알고리즘의 학습 및 정책 수립 과정을 시각적으로 제공하여 학습자가 추상적인 개념을 구체적으로 이해할 수 있도록 돕습니다.
2. **교육 및 연구 지원:**
   - 강화학습을 처음 접하는 학생들이 쉽게 학습할 수 있는 도구 제공.
   - 연구자들이 알고리즘의 동작을 검증하거나 시뮬레이션 결과를 시각적으로 분석하는 데 활용.
3. **사용자 중심 설계:**
   - 직관적인 UI를 통해 복잡한 알고리즘 과정을 쉽게 탐색 가능.

---

## **주요 기능**
1. **Grid World 시뮬레이션:**
   - 에이전트가 Grid World 환경에서 최적의 경로를 학습하는 과정을 시뮬레이션.
2. **강화학습 알고리즘 지원:**
   - Policy Iteration
   - Value Iteration
   - (향후 추가 가능: Q-Learning 등)
3. **시각화 기능:**
   - 상태 값(State Value) 표시.
   - 행동 값(Action Value) 표시.
   - 정책 방향(Policy Arrows) 표시.
   - 보상(Reward) 표시.
4. **인터렉티브 UI:**
   - 알고리즘 선택 및 설정 기능.
   - 시각화 토글 버튼을 통해 표시 항목 선택 가능.
   - 에이전트 수동 제어 및 알고리즘 실행 상태 제어.

---

## **프로젝트 구성**

```plaintext
RL_GridWorld/
├── rl_algorithms/
│   ├── __init__.py
│   ├── core/
│   │   ├── algorithms/          # 강화학습 알고리즘 구현
│   │   ├── rl_env/              # Grid World 환경 정의
│   │   ├── events.py            # 이벤트 정의
│   │   └── __init__.py
│   ├── ui/                      # UI 및 시각화 구현
│   │   ├── components/          # UI 구성 요소
│   │   ├── observers/           # Observer 패턴 구현
│   │   ├── grid_world_viz.py    # 메인 UI 클래스
│   │   └── __init__.py
│   ├── main.py                  # 프로젝트 실행 진입점
├── docs/                        # Sphinx 기반 문서화 파일
│   ├── source/
│   ├── build/
│   └── conf.py
├── requirements.txt             # 프로젝트 의존성 관리
└── README.md                    # 프로젝트 설명 파일
```

## **설치 및 실행 방법**

### **1. 의존성 설치**
Python 3.8+가 설치되어 있어야 합니다.

1. 가상환경 생성 및 활성화:
   ```bash
   python -m venv venv
   venv\Scripts\activate   # Windows
   source venv/bin/activate   # macOS/Linux
   ```
2. 의존성 설치:
  ```bash
  pip install -r requirements.txt
  ```

### **2. 실행**
  ```bash
  python rl_algorithms/main.py
  ```
## **사용 방법**

1. **환경 설정:**
   - `Grid World` 크기, 보상 및 장애물 배치를 코드에서 설정 가능합니다.

2. **강화학습 알고리즘 실행:**
   - UI에서 알고리즘(예: Policy Iteration)을 선택합니다.
   - 정책 평가(Policy Evaluation), 정책 개선(Policy Improvement) 등의 단계를 수동으로 실행하거나 자동으로 진행할 수 있습니다.

3. **시각화 옵션:**
   - 보상, 상태 값, 행동 값, 정책 방향 등 다양한 정보를 선택적으로 표시할 수 있습니다.
   - 시각화 토글 버튼을 통해 원하는 항목만 선택적으로 표시 가능합니다.

---

## **기대 효과**

1. **강화학습 학습 증진:**
   - 강화학습 개념에 대한 직관적인 이해를 제공하여 학습 효율성을 높입니다.

2. **실시간 분석 지원:**
   - 알고리즘의 학습 진행 상태를 실시간으로 확인하여 디버깅 및 성능 분석을 용이하게 합니다.

3. **교육 및 연구 도구로 활용:**
   - 강의 자료, 멘토링, 연구 발표 등 다양한 교육 및 연구 목적으로 활용 가능합니다.

## **향후 개발 계획**

1. **추가 알고리즘 구현:**
   - Q-Learning 및 Model-Free 알고리즘 추가.
   
2. **복잡한 환경 지원:**
   - 더 큰 Grid World 및 다양한 장애물 배치 옵션 추가.
   
3. **학습 데이터 저장 및 시각화:**
   - 학습 진행 상태를 기록하고, 학습 데이터 분석 도구 제공.
