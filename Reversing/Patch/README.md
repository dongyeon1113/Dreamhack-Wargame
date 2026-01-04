# Dreamhack: Patch Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 2
- **Tool:** IDA Free
- **Description:** 가려진 flag가 보이게 어셈블리어를 patch하는 문제

## 2. Static Analysis (정적 분석)
### 2.1. Initial Analysis
flag.exe파일을 먼저 실행해보았더니 아래와같이 flag만 덧칠한것처럼 가려져있는것을 볼 수 있었습니다.
여기서 저는 flag에 덧칠을 하는 함수가 여러번 반복되겠구나라고 추측을 했습니다.

![initialrun](./initialrun)

flag.exe파일을 ida로 열어서 Strings를 확인해보 win32api가 쓰인것을 알 수 있습니다.
Reference: win32api는 프로그램이 윈도우 운영체제(OS)에게 일을 시킬 때 사용하는 공식 명령어 세트입니다.

![FunctionList](./funtionlist)






![DIE Analysis](./DIEanalysis.png)

이후 Ubuntu 환경에서 프로그램을 실행하여 동작을 확인했습니다.

![LINUX Analysis](./ubuntuanalysis.png)

### 2.2. Main Logic Finding & Solution
**Great xD 1 year has passed! The flag is ...** 라는 성공 문자열을 Cross Reference (Xref) 하여 메인 로직이 위치한 함수를 찾았습니다.

핵심 로직은 다음과 같습니다
프로그램은 counter(var_4)에 따라 두 가지 경로로 플래그를 생성하는 구조를 가지고 있습니다.

1. 분기 조건 변경 (cmp [rbp+var_4], 0 -> cmp [rbp+var_4], 5)기존 코드는 counter가 0보다 클 때(jg) 루프로 진입하고, 0 이하일 때 우측 검사 영역으로 분기하여 플래그 획득 경로를 이원화하고 있었습니다. 특정 제약 조건(3조건)을 만족시키기 위해, 기준값을 0에서 5로 변경하여 5보다 클 때만 루프로 진입하도록 패치했습니다.

2. 루프 목표값 검증 (cmp [rbp+var_4], 3h -> cmp [rbp+var_4], 0Ah)루프 내부에서 현재 값이 특정 값과 일치할 때 플래그 출력을 위한 메모리 연산(복호화)이 수행됩니다. 1번 패치로 인해 5 초과의 값만 루프에 진입하므로, 기존 목표값인 3(0x3)에는 도달할 수 없습니다. 따라서 연산이 정상적으로 수행되도록 목표값을 10(0xA)으로 수정했습니다.

3. 즉시 성공 조건 (cmp [rbp+var_4], 5)우측 분기(루프에 진입하지 않는 경우)에서는 값이 5인지 확인합니다. 이 조건이 만족될 경우, 복잡한 반복 연산 없이 즉시 Nice! 문자열을 출력하고 flag_gen 함수를 호출하여 빠르게 플래그를 획득합니다.

4. 카운트 다운 (sub [rbp+var_4], 1)counter 값을 1씩 차감(sub)하고 다시 분기점으로 돌아갑니다. 입력값이 조건에 도달할 때까지 숫자를 줄여나가는 카운트다운 역할을 수행합니다.

![IDA Graph View](./idaanalysis.png)


처음에는 루프 자체를 우회하려 했으나, 루프 내부에서 플래그 생성을 위한 연산이 수행됨을 파악했습니다. 
따라서 2번과같이 패치해 counter가 10일때 복호화 연산을 수행하게 하고 1번과같이 패치해 3번조건을 만족하도록 패치해주었습니다.

## 3. Result
플래그 추출 성공: `DH{389998e56e90e8eb34238948469cecd6dd89c04dce359c345e0b2f3ef9edc66a}`

![Success Screenshot](./flag_success.png)

## 4. Thoughts
처음에는 확장자가 없는 파일을 보고 당황했지만, DiE를 활용해 리눅스 바이너리임을 식별하며 분석을 시작할 수 있었다. 
초기에는 분기문자체를 수정하여 루프를 건너뛰려 했으나, 플래그가 정상적으로 복호화되지 않는 시행착오를 겪었다. 
이를 통해 단순히 흐름을 강제로 우회하는 것이 아니라, **특정조건에서 복호화과정을 무조건 거쳐야한다** 는 점을 깨달았다.
이번 문제를 통해 리버싱에서 무조건적인 분기문 패치는 지양하고, flag를 추출하기 위한 과정을 거치는것이 중요하다는것을 깨달았다.



