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
v5 = key1 ^ (v4 + ((v3 << 7) | (v3 >> 9))) #ROL 7
v3 = (key2 ^ ((v4 << 7) | (v4 >> 9)))& 0xFFFF 
v4 = v5& 0xFFFF
```

python으로 재구성한 암호화 코드입니다.

[Encrypt Code](./encrypt.py)


## 3. Solution
위에서 요약한 각 연산들은 역연산이 가능합니다.

```python
prev_v4 = ROR(v3 ^ key2,7)
temp = (v4^key1)&0xFFFF
diff = (temp - prev_v4) & 0xFFFF
prev_v3 = ROR(diff,7)
v3 = prev_v3
v4 = prev_v4
```

다음은 전체 복호화 코드입니다.
### Full Solver Code
```python
# key 파일을 바이너리 읽기 모드로 열어 바이트 배열로 저장
with open("key", "rb") as f:
    key_data = bytearray(f.read())

# 암호화된 파일(flag.enc)을 바이너리 읽기 모드로 열어 저장
with open("flag.enc", "rb") as f:
    flag_data = bytearray(f.read())

# 복호화된 데이터를 담을 빈 배열 생성 (암호화 데이터와 동일한 크기)
decrypted_data = bytearray(len(flag_data))

def ROR(val, n):
    """
    16비트 정수 기준 오른쪽 순환 이동(Rotate Right) 함수
    val: 값, n: 이동할 비트 수
    """
    max_bits = 16
    return ((val >> n) | (val << (16 - n))) & 0xFFFF

# 데이터를 4바이트씩 묶어서 처리 (Block 단위 복호화)
for i in range(0, len(flag_data), 4):
    
    # 1. 암호화된 데이터의 앞 2바이트를 읽어 v3(16비트 정수)로 변환
    chunk = flag_data[i : i+2]  
    v3 = int.from_bytes(chunk, 'little')

    # 2. 암호화된 데이터의 뒤 2바이트를 읽어 v4(16비트 정수)로 변환
    chunk = flag_data[i+2 : i+4]  
    v4 = int.from_bytes(chunk, 'little')

    # 암호화 과정의 역순으로 3회 반복 (복호화 라운드)
    for j in range(3):
        # 키 데이터를 역순(2 -> 1 -> 0)으로 가져와서 사용
        key_chunk = key_data[4*(2-j):4*(2-j)+2]
        key1 = int.from_bytes(key_chunk, 'little')
        
        key_chunk = key_data[4*(2-j)+2:4*(2-j)+4]
        key2 = int.from_bytes(key_chunk, 'little')

        # --- 복호화 연산 시작 ---
        
        # 1) 현재 v3와 key2를 XOR한 후 7비트 ROR하여 이전 단계의 v4를 복구
        prev_v4 = ROR(v3 ^ key2, 7)
        
        # 2) v4와 key1을 XOR 연산
        temp = (v4 ^ key1) & 0xFFFF
        
        # 3) XOR 결과값에서 복구된 prev_v4를 빼서 차이값을 구함
        diff = (temp - prev_v4) & 0xFFFF
        
        # 4) 차이값을 7비트 ROR하여 이전 단계의 v3를 복구
        prev_v3 = ROR(diff, 7)
        
        # 다음 라운드 계산을 위해 v3, v4 업데이트
        v3 = prev_v3
        v4 = prev_v4

    # 복호화된 16비트 정수들을 다시 바이트(2바이트씩)로 변환하여 결과 배열에 저장
    decrypted_data[i : i+2] = v3.to_bytes(2, 'little')
    decrypted_data[i+2 : i+4] = v4.to_bytes(2, 'little')

# 최종 복호화된 바이트 배열을 문자로 변환하여 화면에 출력
for i in range(0, len(decrypted_data)):
    print(chr(decrypted_data[i]), end='')
```

## 4. Thoughts
ARX(Addition, Rotation, XOR) 구조의 암호화과정을 직접 파이썬으로 구현하며 복호화 로직을 설계해 볼 수 있는 좋은 문제였다.
연산과정들보다 데이터를 처리하는과정이 까다로웠다.(Little Endian 고려)
복호화코드도 연산순서도 고려해야하다보니 체감난이도가 높았다.






