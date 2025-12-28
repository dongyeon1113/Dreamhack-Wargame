# 🛡️ Dreamhack Wargame Write-ups

**리버싱 공부 기록**

이 저장소는 Dreamhack 워게임 문제들을 해결하며 작성한 **분석 보고서 및 소스 코드**를 포함합니다.
단순히 정답(Flag)을 얻는 것이 아니라, 바이너리의 동작 원리를 가장 낮은 단계(Low-Level)에서 이해하는 과정을 기록했습니다.

---

## 🛠️ Analysis Methodology

### No Decompiler Policy
본 프로젝트의 모든 결과물은 **디컴파일러(F5)의 의사 코드(Pseudo-code)를 전혀 참고하지 않고 작성**되었습니다. 저는 리버싱의 기초 체력을 위해 다음과 같은 **Manual Reconstruction** 프로세스를 고수합니다.

1.  **Static Analysis (정적 분석)**
    * IDA Graph View와 Disassembly Text만을 사용하여 제어 흐름(Control Flow)을 파악합니다.
    * 레지스터(`rax`, `rbx`...)의 상태 변화와 스택 프레임(`rsp`, `rbp`) 관리를 추적합니다.

2.  **Logic Reconstruction (논리 재구성)**
    * 분석한 어셈블리 명령어를 기반으로, 원본 C 소스 코드의 로직을 **1:1로 수동 복원**합니다.
    * 이 과정에서 컴파일러의 최적화 패턴, 변수 타입, 구조체 형태를 역추론합니다.

3.  **Inverse Operation (역연산 구현)**
    * 복원된 알고리즘의 수학적 특성을 파악하여, 암호화된 데이터를 복구하는 **Keygen/Solver**를 직접 구현합니다.

---

## 📂 Repository Structure

```bash
├── Reversing/                  # Dreamhack Wargame 문제 풀이 모음
│   ├── 여러문제들/
│   │   ├── README.md           # 상세 분석 노트 (Assembly Logic & Strategy)
│   │   └── solution.c          # 연산(Inverse Operation) 구현 코드
│   │      
│   └── ...
└── README.md                   # 프로젝트 개요 및 분석 방법론 (Methodology)
