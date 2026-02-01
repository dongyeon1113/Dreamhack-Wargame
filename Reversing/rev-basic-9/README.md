# Dreamhack: rev-basic-9 Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 3
- **Tool:** IDA Free, VS Code (Python)
- **Description:** Correct를 출력하는 입력값을 찾는문제

## 2. Static Analysis (정적 분석)
### 2.1. Main Logic Finding
`Correct` 문자열을 Xref하여 메인 검증 함수(`sub_140001000`)를 찾았습니다.
해당 함수를 분석한 결과, 반복문을 순회하며 아래와 같은 검증 로직을 수행하는 것을 파악했습니다.

- i += 8: 반복문이 1씩 증가하지 않고 8씩 건너뜁니다.
  &a1[i]: 함수의 인자로 넘어가는 주소가 a1[0], a1[8], a1[16]... 순서입니다.
  sub_140001000 함수는 입력받은 주소로부터 **8바이트씩** sub_1400010A0함수로 넘기고있습니다. 

- **8바이트씩** 암호화 연산이 끝난 후 **memcmp**를 통해서 **unk_140004000**과 비교하고있습니다.

![IDA Graph View](./idaanalysis1.png)

### 2.2. Assembly to Python (핵심)
분석한 어셈블리 코드를 바탕으로 Python 의사 코드(Pseudo-code)로 복원했습니다. 
암호화 함수(`sub_1400010A0`)를 분석한 결과입니다.

**[Reconstructed Python Code]**
```python

# 암호화 키 (8바이트)
KEY = b"I_am_KEY"

# S-Box 테이블 (메모리 0x140004020 참조)
S_BOX = [ ... ] # 생략

# ROR 함수
def ROR(val, n, bits=8):
    return ((val >> n) | (val << (bits - n))) & ((1 << bits) - 1)

def encrypt_block(block):
    # 총 16번 반복 수행
    for i in range(16):
        # 8바이트 블록 내부를 순회하며 바이트 단위 연산
        for j in range(8):
            
            # S-Box 참조 인덱스 계산 (Key와 현재 바이트를 XOR)
            idx = KEY[j] ^ block[j]
            
            # 다음 바이트 변환
            # (j + 1) & 7 : 인덱스 7을 넘어가면 0으로 
            next_val = block[(j + 1) & 7] + S_BOX[idx]
            
            # 우측으로 5비트 회전 (ROR 5) 후 결과 저장
            block[(j + 1) & 7] = ROR(next_val, 5)

    return block
```

## 3. Solution

암호화 루틴을 분석한 결과, 데이터는 다음과 같은 과정을 거쳐 변환됩니다.
```mermaid
graph LR
    A[Input] -- "+ S_Box" --> B(temp)
    B -- "ROR 5" --> C[Encrypted Data]
```

따라서 복호화(Decryption)는 이 과정을 거꾸로 거슬러 올라가며 역연산을 수행해야 합니다.

```mermaid
graph LR
    C[Encrypted Data] -- "ROL 5" --> B(temp)
    B -- "- S_BOX" --> A[Input]
```

### Full Solver Code
[solution](./solution.py) 파일을 참고하세요.

## 4. Result
플래그 추출 성공: `DH{Reverse__your__brain_;)}`

![Success Screenshot](./flag_success.png)

## 5. Thoughts
드디어 rev-basic 시리즈의 마지막을 풀었다. 이 마지막 문제를 풀기 위해서 레벨2 문제들을 디컴파일러없이 풀면서 어셈블리 독해실력을 키웠다.
레벨 3에 들어오면서 체감난이도가 확 뛴거같다. 이번문제의 요점은 데이터가 어떻게 저장되는지를 파악하는것이었다. 역연산을 짜는데 시간이 좀 걸렸다.
음수가 나오는것을 방지해야지 이 문제가 풀린다.

