# Dreamhack: rev-basic-5 Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 2
- **Tool:** IDA Free, VS Code (C Language)
- **Description:** 사용자 입력의 연속된 두 글자 합을 검증하는 로직을 분석하고, 문자열 끝(NULL)을 기점으로 역순 계산하여 플래그를 복구함

## 2. Static Analysis (정적 분석)
### 2.1. Main Logic Finding
`Correct` 문자열을 Xref하여 메인 검증 함수(`sub_140001000`)를 찾았습니다.
함수 내부는 반복문을 돌며 사용자 입력값의 각 문자를 변환하고 연산하며 기존의 데이터와 비교하고있습니다.

![IDA Graph View](./analysis.png)


### 2.2. Assembly to C Reconstruction (핵심)
어셈블리 코드를 분석하여 C언어로 복원했습니다.
- ~~
- 

**[Assembly Code]**
```assembly

```

**[Reconstructed C Code]**
```c

```

## 3. Solution (풀이 과정)


### Full Solver Code
[solution.c](./solution.c) 파일을 참고하세요.

## 4. Result
플래그 추출 성공: 

![Success Screenshot](./flag_success.png)
