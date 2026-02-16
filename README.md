#  Dreamhack Wargame Write-ups

**리버싱 기초 체력 단련 기록**

이 저장소는 Dreamhack 워게임 문제들을 해결하며 작성한 **분석 보고서 및 솔버(Solver)** 를 담고 있습니다.  
단순히 Flag를 얻는 것에 그치지 않고 바이너리의 동작 원리를 **Low-Level** 단계에서 완전히 이해하는 과정을 기록합니다.

---

##  Analysis Approach: "No Decompiler"

분석 시 디컴파일러(`F5`)에 의존하기보다, 최대한 **어셈블리 단계에서 분석**하며 기본기를 다지는 연습을 하고 있습니다.

### 1. Static Analysis (정적 분석)
* **Control Flow 파악:** IDA Graph View와 Disassembly Text만으로 프로그램의 전체 흐름을 읽습니다.
* **Stack & Register 추적:** 레지스터의 상태 변화와 스택 프레임의 움직임을 직접 보고 확인합니다.

### 2. Logic Reconstruction (C, python복원)
* **1:1 수동 복원:** 분석한 기계어 논리를 바탕으로 원본 C, python 코드를 직접 재구성합니다.

### 3. Solver Implementation (역연산)
* **Algorithm Analysis:** 복원된 알고리즘의 수학적 특성을 파악합니다.
* **solver code 구현:** 암호화된 데이터를 복구하거나 플래그를 추출하는 **Solver** 코드를 직접 작성합니다.

---

## 📂 Repository Structure

```bash
├── Reversing/                  # Dreamhack Wargame 문제 풀이 모음
│   ├── Problems/
│   │   ├── README.md           # 상세 분석 노트 (Assembly Logic & Strategy)
│   │   └── solution.c          # 연산(Inverse Operation) 구현 코드
│   │      
│   └── ...
└── README.md                   # 프로젝트 개요 및 분석 방법론 (Methodology)
