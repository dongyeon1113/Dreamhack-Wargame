# Dreamhack: ezmix Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 2
- **Tool:** IDA Free, VS Code (Python), pwndbg
- **Description:** 사용자 입력값을 특정 규칙에 따라 변형하여 output.bin을 생성하는 바이너리를 분석하여 복호화 하는 문제

## 2. Static Analysis (정적 분석)
### 2.1. Main Logic Finding 
메인 로직을 디컴파일하면 program.bin에서 2바이트씩 읽어와 v3(Opcode)와 v6(Value) 쌍으로 명령을 수행하는 구조를 확인할 수 있습니다.
```C
  // 메인 루프 요약
for ( i = 0; ; i += 2 )
{
    // ... 생략 ...
    v6 = *(_BYTE *)((int)i + 1LL + a1);       // Value (연산에 쓰일 값)
    v3 = *(unsigned __int8 *)((int)i + a1);   // Opcode (연산 종류)

    if ( v3 == 4 ) { // 사용자 입력 
        printf("Insert your string: ");
        fgets(a3, 256, stdin);
        v7 = strlen(a3);
    }
    else {
        switch ( v3 ) {
            case 3: sub_1301(sub_12C2, v6, a3, v7); break; // ROR
            case 1: sub_1301(sub_1289, v6, a3, v7); break; // XOR
            case 2: sub_1301(sub_12A7, v6, a3, v7); break; // ADD
        }
    }
}
```
### 2.2. Handler Functions
sub_1301 함수는 일종의 Dispatcher 역할을 하며, 인자로 전달된 하위 함수(sub_12C2, sub_1289, sub_12A7)를 호출하여 모든 입력 문자열(a3)에 대해 1바이트씩 연산을 적용합니다.

각 서브 함수의 로직은 다음과 같습니다:
- sub_12C2: (a1 >> a2) | (a1 << (8 - a2)) 형태의 Bitwise Rotate Right(ROR) 연산 수행.

- sub_1289: 두 값을 더하는 Addition 연산 수행.

- sub_12A7: 두 값을 XOR 하는 Exclusive OR 연산 수행.

## 2.3. Reconstructing Encryption Logic 
위 내용들을 전부 합쳐서 암호화 로직을 python으로 재구성했습니다.
```python
def encrypt_ror(val, data, length):
    shift = val & 7
    for i in range(length):
        # 데이터를 오른쪽으로 회전 (8비트 기준)
        data[i] = ((data[i] >> shift) | (data[i] << (8 - shift))) & 0xFF


def encrypt_add(val, data, length):
    for i in range(length):
        # 특정 값을 더함 (Overflow 방지를 위해 0xFF 마스킹)
        data[i] = (data[i] + val) & 0xFF

def encrypt_xor(val, data, length):
    for i in range(length):
        # 특정 값과 XOR 연산
        data[i] = (data[i] ^ val) & 0xFF

# a1: program.bin 데이터, a3: Input, v7: Input 길이
for i in range(2, 0x202, 2):
    opcode = a1[i]      # v3: 연산 종류
    value = a1[i + 1]   # v6: 연산에 사용될 value

    if opcode == 3:
        encrypt_ror(value, a3, v7)
    elif opcode == 2:
        encrypt_add(value, a3, v7)
    elif opcode == 1:
        encrypt_xor(value, a3, v7)


```



## 3. Solution
암호화 로직이 program.bin의 명령을 순차적으로 적용하는 방식이므로 복호화를 위해서는 다음 두 가지 핵심 원칙을 적용해야 합니다.

연산의 역순: program.bin의 마지막 명령부터 처음 방향으로 거꾸로 거슬러 올라가며 연산합니다. (range의 역순 처리)

역연산 적용:

- ADD의 역연산: SUBTRACT (파이썬에서는 - val & 0xFF)

- ROR의 역연산: ROL (왼쪽 회전)

- XOR의 역연산: XOR (자기 자신과 다시 XOR)

### Full Solver Code
```python
with open("output.bin", "rb") as f:
    a3 = bytearray(f.read())
with open("program.bin", "rb") as f:
    a1 = bytearray(f.read())

a1 = a1[2:] # 앞의 헤더 2바이트 제거

def sub_12C2(v3, a3, v7): # Rotate Left
    n = v3 & 7
    for i in range(v7):
        a3[i] = ((a3[i] << n) & 0xFF) | (a3[i] >> (8 - n))

def sub_1289(v3, a3, v7): # Subtract
    for i in range(v7):
        a3[i] = (a3[i] - v3) & 0xFF

def sub_12A7(v3, a3, v7): # XOR
    for i in range(v7):
        a3[i] = (a3[i] ^ v3) & 0xFF

v7 = len(a3)

# 인덱스를 뒤에서부터 2칸씩 점프하며 가져옴
for i in range(len(a1) - 2, -1, -2):
    v6 = a1[i]      # 명령 (1, 2, 3)
    v3 = a1[i + 1]  # 연산에 쓸 값
    
    if v6 == 3:
        sub_12C2(v3, a3, v7)
    elif v6 == 1:
        sub_1289(v3, a3, v7)
    elif v6 == 2:
        sub_12A7(v3, a3, v7)

# 결과 출력
for i in range(v7):
    print(chr(a3[i]), end='')
```



## 4. Result
플래그 추출 성공: DH{4DD_X0R_R07473_34S1LY_R3V3RS1BL3}

![Success Screenshot](./flag_success.png)

## 5. Thoughts
레벨3 문제를 풀다가 너무 막혀서 다시 내 실력이 부족하다고 여기고 레벨2로 돌아왔다. 아직 레벨2도 좀 시간이 걸리는것을 보니
레벨3으로 넘어갈때가 아닌가보다. 조금 더 역연산 구현과 코딩연습을 하고 넘어가야겠다.





