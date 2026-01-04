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

### sub_4011EF Stack Frame & Register Setup
| Register / Memory | Variable Name (내 방식) | Description |

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

### sub_401263 Stack Frame & Register Setup
| Register / Memory | Variable Name (My Analysis) | Description |

| `rdi` | `s1` | Input string pointer |

| `rsi` | `val` | Integer value |

| `[rbp+var_18]` | `s1_ptr` | Saved pointer to input string |

| `[rbp+var_1C]` | `add_val` | The integer value to add |

| `[rbp+var_4]` | `index` | Loop counter (initialized to 0) |

### Assembly Logic 
**Loop Condition:** Iterate 32 times 
```assembly
mov     eax, [rbp+var_4]      ; eax = index
movsxd  rdx, eax              ; rdx = index 
mov     rax, [rbp+var_18]     ; rax = s1_ptr
add     rax, rdx              ; rax = s1_ptr + index
movzx   ecx, byte ptr [rax]   ; ecx = s1[index] 
mov     eax, [rbp+var_4]      ; eax = index 
movsxd  rdx, eax              ; rdx = index
mov     rax, [rbp+var_18]     ; rax = s1_ptr
add     rax, rdx              ; rax = s1_ptr + index
movzx   edx, [rbp+var_1C]     ; edx = add_val 
add     edx, ecx              ; edx = add_val + s1[index]
mov     [rax], dl             ; s1[index] = add_val + s1[index]
add     [rbp+var_4], 1        ; index++

conclusion: s1[i] = s1[i] + add_val
```

### sub_4012B0 Stack Frame & Register Setup
| Register / Memory | Variable Name (My Analysis) | Description |

| `rdi` | `s1` | Input string pointer |

| `rsi` | `val` | Integer value |

| `[rbp+var_18]` | `s1_ptr` | Saved pointer to input string |

| `[rbp+var_1C]` | `sub_val` | The integer value to subtract |

| `[rbp+var_4]` | `index` | Loop counter (initialized to 0) |

### Assembly Logic 
**Loop Condition:** Iterate 32 times 
```assembly
mov     eax, [rbp+var_4]      ; eax = index
movsxd  rdx, eax              ; rdx = index
mov     rax, [rbp+var_18]     ; rax = s1_ptr
add     rax, rdx              ; rax = s1_ptr + index
movzx   eax, byte ptr [rax]   ; eax = s1[index] 
mov     edx, [rbp+var_4]      ; edx = index
movsxd  rcx, edx              ; rcx = index
mov     rdx, [rbp+var_18]     ; rdx = s1_ptr
add     rdx, rcx              ; rdx = s1_ptr + index 
sub     al, [rbp+var_1C]      ; al = s1[index] - sub_val 
mov     [rdx], al             ; s1[index] = s1[index] - sub_val
add     [rbp+var_4], 1        ; index++

conclusion: s1[i] = s1[i] - sub_val
```


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
플래그 추출 성공: `DH{Roll_the_left!_Roll_the_right!}`

![Success Screenshot](./flag_success.png)

## 5. Thoughts



