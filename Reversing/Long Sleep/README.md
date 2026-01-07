# Dreamhack: Long Sleep Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 2
- **Tool:** IDA Free, ununtu,DIE
- **Description:** 실행 후 대기상태에 빠지는 프로그램을 플래그를 출력하게 만드는 문제

## 2. Static Analysis (정적 분석)
### 2.1. Initial Analysis
제공된 **prob** 파일에 확장자가 없어 파일 형식을 식별하기 위해 정적 분석 도구인 DIE (Detect It Easy) 를 사용했습니다. 분석 결과, 해당 파일이 리눅스 실행 파일(ELF 64-bit)임을 확인했습니다.

Reference: DIE는 실행 파일의 컴파일러, 패커, 파일 형식 등을 상세히 알려주는 도구입니다.

![dieanalysis](./dieanalysis.png)

이후 ubuntu를 사용해 리눅스환경에서 프로그램을 실행하여 동작을 확인했습니다.

![pwndbg](./initiarun.png)

**Wait! I'm generating flag!!** 라는 문자열이 출력되고 프로그램이 계속 실행중인것을 확인할 수 있습니다.
이에 저는 프로그램을 멈추는 sleep계열의 시스템 콜이나 무한 루프가 있을것이라고 가설을 내렸습니다.

### 2.2 Main Logic Finding
**Wait! I'm generating flag!!**  문자열을 Cross Reference (Xref) 하여 메인 로직이 위치한 함수를 찾았습니다.

프로그램은 **Wait! I'm generating flag!!** 까지만 실행하고 **Here's your flag~~** 까지는 출력을 못 하니 
**call sub_1411** 에서 프로그램을 멈추는 역할을 하는 함수가 숨어있을 것이라 판단했습니다.

![idaanalysis](./idaanalysis1.png)

분석과정에서 **nanosleep** 이라는 처음보는 함수를 발견했습니다. 

**nanosleep** : 리눅스 시스템 콜(System Call) 중 하나, 프로그램의 실행을 지정된 시간만큼 중지시키는 함수. 
일반적인 sleep() 함수가 초 단위로 제어하는 것과 달리, 나노초 단위의 시간 제어가 가능

![idaanalysis](./nanosleep.png)

**nanosleep**이 프로그램을 멈추는 핵심함수라고 판단하여 **nanosleep**을 호출하는 **syscall**






## 3. Solution (풀이 과정)
암호화 순서를 분석하여 도출한 역방향 복호화 표입니다.
암호화와 반대로 복호화를하려면 함수실행 순서도 반대로 연산도 역연산으로 수행해야합니다.

| 순서 | 암호화 흐름 (Forward) | 연산 | $\leftrightarrow$ | 복호화 흐름 (Solver) | 역연산 수행 |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **1** | `sub_4011EF` (Key: `unk_402068`) | XOR | $\leftrightarrow$ | **Step 7** (마지막) | **XOR** |
| **2** | `sub_401263` (Val: `31`) | ADD | $\leftrightarrow$ | **Step 6** | **SUB** `31` |
| **3** | `sub_4012B0` (Val: `90`) | SUB | $\leftrightarrow$ | **Step 5** | **ADD** `90` |
| **4** | `sub_4011EF` (Key: `unk_40206D`) | XOR | $\leftrightarrow$ | **Step 4** | **XOR** |
| **5** | `sub_4012B0` (Val: `77`) | SUB | $\leftrightarrow$ | **Step 3** | **ADD** `77` |
| **6** | `sub_401263` (Val: `243`) | ADD | $\leftrightarrow$ | **Step 2** | **SUB** `243` |
| **7** | `sub_4011EF` (Key: `unk_402072`) | XOR | $\leftrightarrow$ | **Step 1** (시작) | **XOR** |

### Full Solver Code
[solution.c](./solution.c) 파일을 참고하세요.

## 4. Result
플래그 추출 성공: `DH{9ce745c0d5faaf29b7aecd1a4a72bc86}`

![Success Screenshot](./flag_success.png)

## 5. Thoughts
남들이 디컴파일러(F5) 한 번으로 쉽게 해결할 문제를 어셈블리어 한 줄 한 줄 직접 뜯어보며 분석하다 보니 시간도 오래 걸리고 **이 방식이 정말 효율적인가?** 하는 회의감도 들었다.
하지만 이번 문제를 풀면서 그동안의 끈기 있는 시도가 결코 헛되지 않았음을 깨달았다. 전에는 흐릿하게만 보이던 스택 프레임 구조가 머릿속에 명확히 그려지기 시작했고 이해가 안 되던 어셈블리 명령어들이 
문맥으로 연결되어 읽히는 것을 경험했다 마치 책을 읽는것처럼.
코드 독해 속도가 빨라진 내 자신을 보며 도구에 의존하기 전에 **기본기**를 다지는 과정이 얼마나 중요한지 다시 한번 확신하게 됐다.



