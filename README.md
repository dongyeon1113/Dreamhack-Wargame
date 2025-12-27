![C](https://img.shields.io/badge/c-%2300599C.svg?style=for-the-badge&logo=c&logoColor=white)
![Assembly](https://img.shields.io/badge/Assembly-555555?style=for-the-badge&logo=asm&logoColor=white)
![IDA Pro](https://img.shields.io/badge/IDA%20Pro-2F2F2F?style=for-the-badge&logo=idapro&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
# Dreamhack Rev-Engineering Archive

**Archived by Kang Dong-yeon** *Sungkyunkwan University, Dept. of Software* *Former ROK Army Information Security Squad (CERT)*

---

## 🛠 Methodology

본 리포지토리는 리버싱의 본질적인 이해를 돕기 위해 **Static Analysis(정적 분석)** 위주로 수행된 문제 풀이를 기록합니다.

### 🚫 No Decompiler Policy
편리한 디컴파일 도구(F5) 뒤에 숨겨진 로직을 놓치지 않기 위해, **직접 어셈블리 명령어(Opcode)를 해석**하고 이를 High-Level Language(C/Python)로 포팅하는 훈련을 수행합니다.

1.  **Analyze:** IDA Graph View를 통한 제어 흐름 및 레지스터 상태 분석
2.  **Reconstruct:** 어셈블리 로직을 C언어 구조로 1:1 재구현 (변수 타입 및 구조체 추론)
3.  **Solve:** 복원된 알고리즘의 역연산 로직을 통해 플래그 도출

이러한 **Manual Reconstruction** 과정은 바이너리의 동작 원리를 가장 정확하게 파악하는 방법이자, 리버서로서 갖춰야 할 견고한 기초 체력입니다.
