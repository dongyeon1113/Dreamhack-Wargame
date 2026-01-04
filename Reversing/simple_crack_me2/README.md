# Dreamhack: simple_crack_me2 Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 2
- **Tool:** IDA Free, VS Code (C Language), pwndbg
- **Description:** Correct를 출력해내는 사용자 입력값을 찾는 문제

## 2. Static Analysis (정적 분석)
### 2.1. Initial Analysis
제공된 simple_crack_me2 파일에 확장자가 없어 파일 형식을 식별하기 위해 정적 분석 도구인 DIE (Detect It Easy) 를 사용했습니다. 분석 결과, 해당 파일이 리눅스 실행 파일(ELF 64-bit)임을 확인했습니다.

Reference: DIE는 실행 파일의 컴파일러, 패커, 파일 형식 등을 상세히 알려주는 도구입니다.

![dieanalysis](./dieanalysis.png)

이후 pwndbg를 사용해 리눅스환경에서 프로그램을 실행하여 동작을 확인했습니다.

Reference: pwndbg는 리눅스 터미널 디버거인 GDB(GNU Debugger)를 해킹과 리버싱에 최적화된 형태로 개조해 주는 강력한 플러그인입니다.

![pwndbg](./pwndbg.png)

### 2.2 Main Logic Finding
**Correct!** 성공 문자열을 Cross Reference (Xref) 하여 메인 로직이 위치한 함수를 찾았습니다.

![idaanalysis](./idaanalysis.png)

s1은 입력문자열이고 4011EF(s1,unk_402068) -> 401263(s1,31) -> 4012B0(s1,90) -> 4011EF(s1,unk_40206D)
-> 4012B0(s1,77) -> 401263(s1,243) -> 4011EF(s1,unk_402072) -> memcmp(s1,s2,32) 순서대로 진행됩니다.

s1이 여러 암호화 함수들을 거쳐 s2와 비교되는것을 확인했습니다.
correct를 출력하는 입력값을 알아내기 위해서 각 암호화 함수들을 분석했습니다.

### 4011EF Stack Frame & Register Setup
| Register / Memory | Variable Name (My Analysis) | Description |
| `rsi` | `unk` | Key string pointer |
| `rdi` | `s1` | Input string pointer |
| `[rbp+var_18]` | `s1_ptr` | Saved pointer to input string |
| `[rbp+var_20]` | `key_ptr` | Saved pointer to key string |
| `[rbp+var_8]` | `key_len` | Length of the key string |
| `[rbp+var_C]` | `index` | Loop counter (initialized to 0) |
### Assembly Logic 
**Loop Condition:** Iterate 32 times 
```assembly
mov     eax, [rbp+var_C]      ; eax = index
movsxd  rdx, eax              ; rdx = index 
mov     rax, [rbp+var_18]     ; rax = s1_ptr
add     rax, rdx              ; rax = s1_ptr + index
movzx   ecx, byte ptr [rax]   ; ecx = s1[index] 
mov     eax, [rbp+var_C]      ; eax = index
cdqe                          ; Convert Double to Quad 
mov     edx, 0                ; edx = 0 
div     [rbp+var_8]           ; div by key_len
                              ; Result: rax = 몫, rdx = 나머지 
mov     rax, [rbp+var_20]     ; rax = key_ptr
add     rax, rdx              ; rax = key_ptr + remainder
movzx   edx, byte ptr [rax]   ; edx = key[index % key_len]
mov     eax, [rbp+var_C]      ; eax = index
movsxd  rsi, eax              ; rsi = index
mov     rax, [rbp+var_18]     ; rax = s1_ptr
add     rax, rsi              ; rax = s1_ptr + index
xor     edx, ecx              ; edx = key[index % key_len] ^ s1[index] 
mov     [rax], dl             ; s1[index] = key[index % key_len] ^ s1[index] 
add     [rbp+var_C], 1        ; index++

conclusion: s1[i] = s1[i] ^ key[index % key_len]
```



## 3. Solution (풀이 과정)
정적 분석을 통해 파악한 암호화 루틴은 Input -> ROL -> XOR -> Data 순서로 진행됩니다. 따라서 원본 플래그(Input)를 복구하기 위해서는 연산 순서를 역순으로 뒤집고, 각 연산의 역함수(Inverse Function)를 적용해야 합니다. ex) ROL대신 ROR적용

![역연산로직그림](./inverse_logic_flow.png)

Step 1 (XOR 복구): XOR 연산의 역연산은 자기 자신이므로, 데이터(Data)에 인덱스(i)를 다시 XOR 합니다.

Step 2 (Rotate 복구): ROL(왼쪽 회전)의 역연산은 ROR(오른쪽 회전) 이므로, Step 1의 결과를 (i & 7)만큼 오른쪽으로 회전시킵니다.

### Full Solver Code
[solution.c](./solution.c) 파일을 참고하세요.

## 4. Result
플래그 추출 성공: `DH{Roll_the_left!_Roll_the_right!}`

![Success Screenshot](./flag_success.png)

## 5. Thoughts
시리즈의 후반부로 갈수록 어셈블리 코드의 복잡도가 높아짐을 체감한다. 이번 문제에서 ROL과 XOR이라는 핵심 암호화 로직은 성공적으로 파악하여 C언어로 복원했지만, 분석 과정에서 **스택 프레임 초기화 및 메모리 정리**와 같은 점을 실제 로직으로 오인하여 시간을 소모했다.
모든 어셈블리 명령어를 해석하려 하기보다, 전체적인 흐름을 먼저 파악하는 것의 중요성을 깨달았다. 또한, 정적 분석(Static Analysis)만으로는 메모리 값의 변화를 추적하는 데 한계가 있음을 느꼈다. 앞으로는 **x64dbg와 같은 동적 분석 도구**를 적극 도입하여 좀 더 발전해야겠다.


