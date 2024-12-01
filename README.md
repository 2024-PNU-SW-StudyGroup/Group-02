# **Grid World Reinforcement Learning Visualizer**

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
project_root/
├── src/
│   ├── core/
│   │   ├── algorithms/          # 강화학습 알고리즘 구현
│   │   └── env/                 # Grid World 환경 정의
│   ├── ui/                      # UI 및 시각화 구현
│   │   ├── components/          # UI 구성 요소
│   │   └── observers/           # Observer 패턴 구현
│   └── main.py                  # 프로젝트 실행 진입점
├── requirements.txt             # 프로젝트 의존성 관리
└── README.md                    # 프로젝트 설명 파일
