# Dreamhack: Patch Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 2
- **Tool:** IDA Free
- **Description:** 가려진 Flag가 보이도록 바이너리를 Patch하는 문제

## 2. Static Analysis (정적 분석)
### 2.1. Initial Analysis
문제 파일인 flag.exe를 실행해보니, 아래 이미지와 같이 플래그가 있어야 할 위치가 검은색 선들로 덧칠된 것처럼 가려져 있었습니다.
이 현상을 관찰하고, **플래그 위에 덧칠하는 함수가 반복적으로 호출되고 있을 것이다**이라는 초기 가설을 세웠습니다.

![initialrun](./initialrun.png)

가설을 검증하기 위해 IDA로 파일을 열어 정적 분석을 시작했습니다. 

프로그램이 어떤 기능을 사용하는지 파악하고자 Strings 탭을 확인한 결과, 다수의 Win32 API 함수들이 사용된 것을 볼 수 있었습니다.

함수 목록 중에서 저는 특히 **GdipDrawLine** 이라는 함수에 주목했습니다.

**GdipDrawLine**함수는 **두 점을 잇는 직선**을 그리는 함수로 연속해서 호출한다면 문제처럼 마구 칠해서 가리는 용도로 쓸 수 있을거라 판단했습니다.

Reference: **win32api는 프로그램이 윈도우 운영체제(OS)에게 특정 작업(화면 출력, 창 제어, 파일 읽기 등)을 요청할 때 사용하는 공식 함수 인터페이스입니다.**

![FunctionList](./functionlist.png)

### 2.2. Main Logic Finding & Solution
**GdipDrawLine** 함수를 Cross Reference (Xref) 하여 메인 로직이 위치한 함수를 찾았습니다.

![sub_7FF68E8D2B80](./sub_7FF68E8D2B80.png)

핵심 로직은 다음과 같습니다. 아래 그림을 보면 **sub_7FF68E8D2B80**함수가 반복적으로 호출되는것을 볼 수 있습니다.

![RepeatedFunctionCall](./RepeatedFunctionCall.png)

**sub_7FF68E8D2B80**이 flag를 가리며 덧칠을 하는 함수라고 판단하고 처음 호출되는 **sub_7FF68E8D2B80**에 breakpoint를 설정하고
디버깅(f9)해보았습니다.

![breakpoint](./breakpoint.png)

아래사진과같이 한 줄로 덧칠하는 것을 확인할 수 있었습니다.

![debug](./debug.png)






## 3. Result
플래그 추출 성공: `DH{389998e56e90e8eb34238948469cecd6dd89c04dce359c345e0b2f3ef9edc66a}`

![Success Screenshot](./flag_success.png)

## 4. Thoughts
처음에는 확장자가 없는 파일을 보고 당황했지만, DiE를 활용해 리눅스 바이너리임을 식별하며 분석을 시작할 수 있었다. 
초기에는 분기문자체를 수정하여 루프를 건너뛰려 했으나, 플래그가 정상적으로 복호화되지 않는 시행착오를 겪었다. 
이를 통해 단순히 흐름을 강제로 우회하는 것이 아니라, **특정조건에서 복호화과정을 무조건 거쳐야한다** 는 점을 깨달았다.
이번 문제를 통해 리버싱에서 무조건적인 분기문 패치는 지양하고, flag를 추출하기 위한 과정을 거치는것이 중요하다는것을 깨달았다.



