# Dreamhack: My ARX Cipher Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 3
- **Tool:** IDA Free, VS Code (Python)
- **Description:** 주어진 key를 바탕으로 평문파일을 암호화 하는 문

## 2. Static Analysis (정적 분석)
### 2.1. Main Logic Finding 
메인 함수를 디컴파일 한 결과입니다.
```C
  __int64 __fastcall main(int a1, char **a2, char **a3)
{
  __int64 v4; // [rsp+1Ch] [rbp-14h] BYREF
  int v5; // [rsp+24h] [rbp-Ch]
  unsigned __int64 v6; // [rsp+28h] [rbp-8h]

  v6 = __readfsqword(0x28u);
  if ( a1 == 4 )
  {
    v4 = 0LL;
    v5 = 0;
    if ( (unsigned int)sub_1229(a2[1], &v4) )
    {
      if ( (unsigned int)sub_1381(&v4, a2[2], a2[3]) )
      {
        puts("Encryption was successful");
        return 0LL;
      }
      else
      {
        puts("Failed to encrypt");
        return 1LL;
      }
    }
    else
    {
      puts("Failed to read key");
      return 1LL;
    }
  }
  else
  {
    printf("How to use: %s <key_file> <input_file> <output_file>\n", *a2);
    return 1LL;
  }
}

```
puts 메시지로부터 sub_1229는 키를 읽어오는 함수이고, sub_1381은 암호화 함수임을 알 수 있었습니다.

먼저 sub_1229부터 디컴파일 해보았습니다.
```C
__int64 __fastcall sub_1229(const char *a1, void *a2)
{
  FILE *stream; // [rsp+18h] [rbp-8h]

  stream = fopen(a1, L"rw");
  if ( stream )
  {
    if ( fread(a2, 2u, 6u, stream) == 6 )
      return 1;
    fclose(stream);
  }
  return 0;
}
```
a1은 main의 argv[1]이므로 키 파일의 이름임을 알 수 있습니다. (실행 예시: ./encryptor key input output)

이를 fopen으로 연 뒤 fread를 통해 총 12바이트를 읽어오는 것을 볼 수 있습니다.

### 2.2. Encryption
암호화 함수 sub_1381을 디컴파일 해보았습니다.
```C
__int64 __fastcall sub_1381(__int64 a1, const char *a2, const char *a3)
{
  FILE *stream; // [rsp+30h] [rbp-20h]
  FILE *v6; // [rsp+38h] [rbp-18h]
  int s; // [rsp+44h] [rbp-Ch] BYREF
  unsigned __int64 v8; // [rsp+48h] [rbp-8h]

  v8 = __readfsqword(0x28u);
  stream = fopen(a2, L"rw");
  if ( !stream )
    return 0LL;
  v6 = fopen(a3, L"w");
  if ( !v6 )
  {
    fclose(stream);
    return 0LL;
  }
  for ( s = 0; ; fwrite(&s, 2uLL, 2uLL, v6) )
  {
    memset(&s, 0, sizeof(s));
    if ( !(unsigned int)fread(&s, 1uLL, 4uLL, stream) )
      break;
    sub_129F(a1, &s);
  }
  return 1LL;
}

```
stream은 평문 파일(input)에 대한 디스크립터 v6은 암호문을 담을 파일임을 알 수 있습니다.

fread를 통해 평문 파일로부터 4바이트씩 읽어와 sub_129F를 거친 후 fwrite를 통해 이 s 값을 암호문 파일에 적는 것을 알 수 있었습니다.

sub_129F을 디컴파일 한 결과입니다.

```C
__int64 __fastcall sub_129F(__int64 a1, unsigned __int16 *a2)
{
  __int64 result; // rax
  unsigned __int16 v3; // [rsp+16h] [rbp-Ah]
  unsigned __int16 v4; // [rsp+18h] [rbp-8h]
  unsigned __int16 v5; // [rsp+1Ah] [rbp-6h]
  int i; // [rsp+1Ch] [rbp-4h]

  v3 = *a2;
  v4 = a2[1];
  for ( i = 0; i <= 2; ++i )
  {
    v5 = *(_WORD *)(4LL * i + a1) ^ (v4 + ((v3 << 7) | (v3 >> 9)));
    v3 = *(_WORD *)(2 * (2 * i + 1LL) + a1) ^ ((v4 << 7) | (v4 >> 9));
    v4 = v5;
  }
  *a2 = v3;
  result = v4;
  a2[1] = v4;
  return result;
}

```
a1은 12바이트의 키 값을 담고 있고, a2는 평문을 담고 있습니다. 

for 문 안의 내용을 요약해보았습니다.

```python
for j in range(3):
        key_chunk = key_data[4*j:4*j+2]
        key1=int.from_bytes(key_chunk, 'little')
        key_chunk = key_data[4*j+2:4*j+4]
        key2=int.from_bytes(key_chunk, 'little')
        
        v5 = key1 ^ (v4 + ((v3 << 7) | (v3 >> 9)))
        v3 = (key2 ^ ((v4 << 7) | (v4 >> 9)))& 0xFFFF
        
        v4 = v5& 0xFFFF
```
[Encrypt Code](./encrypt.py)

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






