# Dreamhack: rev-basic-9 Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 3
- **Tool:** IDA Free, VS Code (Python)
- **Description:**
  
  실행파일은 text_in.txt를 읽어 커스텀 Base64 테이블을 이용해 인코딩한 뒤 text_out.txt로 저장하는 동작을 수행
  
  주어진 text_in.txt와 text_out.txt 쌍을 분석하여 **Table** 을 먼저 복구

  복구한 테이블을 이용해 flag_out.txt를 역연산하여 플래그를 찾아내는 문제

## 2. Static Analysis (정적 분석)
### 2.1. Main Logic Finding 
- **sub_1289** 함수가 핵심 인코딩 로직을 담당

- 입력값을 3바이트씩 읽어서 복잡한 비트 연산을 거쳐 4글자로 변환

- Base64 알고리즘이지만 표준 테이블이 아닌 byte_4040를 참조

**sub_1289** 함수 도입부를 분석하던 중 프로그램의 실행 인자를 처리하는 로직에서 중요한 단서를 발견
 
```c
fwrite("Usage : ./baseball <table filename> <input filename>\n", 1u, 0x35u, stderr);
stream = fopen(a2[1], "rb");
fread(byte_4040, 65u, 1u, stream);
```

Usage 문자열: 프로그램 실행 시 첫 번째 인자로 **table filename** 을 요구

데이터 로드: fread 함수를 통해 해당 파일에서 65바이트를 읽어 전역 변수 **byte_4040** 에 저장

결론: **table** 파일의 data가 **byte_4040**에 저장

### 2.2. Assembly to Python (핵심)
- C언어로 작성된 sub_1289 함수의 핵심 비트 연산 로직을 Python으로 재구성하면 다음과 같음

**[Reconstructed Python Code]**
```python
# 입력 3바이트 -> 출력 4바이트 변환 로직
# C언어의 포인터 연산을 배열 인덱싱으로 변환

idx1 = in_chunk[0] >> 2
idx2 = ((in_chunk[1] >> 4) | (16 * in_chunk[0]) & 0x30)
idx3 = ((in_chunk[2] >> 6) | (4 * in_chunk[1]) & 0x3C)
idx4 = in_chunk[2] & 0x3F

# 위 인덱스를 이용해 table에서 값을 가져옴
out[0] = table[idx1]
out[1] = table[idx2]
out[2] = table[idx3]
out[3] = table[idx4]
```

## 3. Solution
### 3.1. Recovering Table
text_in.txt과 text_out.txt를 활용하여 테이블 byte_4040을 복구한

- 핵심 아이디어: 인코딩 식을 역으로 이용하여, table[계산된_인덱스] = 암호문_문자 형태로 매핑

- 주의점: 파일의 줄바꿈(\n)이나 패딩(=) 문자는 인덱스 계산을 어긋나게 하므로 전처리 과정에서 제거

[make_table](./make_table.py) 파일을 참고하세요.

### 3.2. Decode Flag (Bitwise Operation)
복구된 테이블을 역참조(index())하고 비트연산을 통해 6bit x 4를 8bit x 3으로 만들어야함

[Key Point: C vs Python] 
- Python은 정수형의 크기 제한이 없으므로, 왼쪽 시프트(<<) 연산 시 상위 비트가 잘려나가지 않고 값이 계속 커짐
  
- 따라서 반드시 & 0xFF 등의 마스킹을 통해 불필요한 비트를 제거해줘야 함
  
**[Important Decoding Code]**
```python
# val1~4는 테이블에서의 인덱스 값 (0~63)

# val1의 6비트 + val2의 상위 2비트
b1 = (val1 << 2) | (val2 >> 4)

# val2의 하위 4비트 + val3의 상위 4비트
# val2 & 0x0F를 하지 않으면 앞쪽 비트 값이 남아서 값이 커짐
b2 = ((val2 & 0x0F) << 4) | (val3 >> 2)

# val3의 하위 2비트 + val4의 6비트
b3 = ((val3 & 0x03) << 6) | val4
```

### Full Solver Code
[solution](./solution.py) 파일을 참고하세요.

## 4. Result
플래그 추출 성공: DH{Did you know how base64 works}

![Success Screenshot](./flag_success.png)

## 5. Thoughts
두번째 레벨 3 문제를 풀었다. table 복구는 생각보다 수월했지만 가장 기본적인 파이썬에서의 정수형을 생각하지않고 계산해서 
복호화 과정에서 오래걸렸다. 레벨이 올라오면서 기술이 필요하다기보다는 누가 기본이 가장 잘 되어있는지를 보는것같다.
항상 기초부터 차근차근 생각해야겠다.



