# Dreamhack: Secret Message Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 2
- **Tool:** IDA Free, VS Code (Pyhon), Ubuntu, DIE
- **Description:** 인코딩된 파일을 분석하여 원본 이미지를 알아내는 문제

## 2. Static Analysis (정적 분석)
### 2.1. Initial Analysis
제공된 prob 파일에 확장자가 없어 파일 형식을 식별하기 위해 정적 분석 도구인 DIE (Detect It Easy) 를 사용했습니다. 분석 결과, 해당 파일이 리눅스 실행 파일(ELF 64-bit)임을 확인했습니다.

Reference: DIE는 실행 파일의 컴파일러, 패커, 파일 형식 등을 상세히 알려주는 도구입니다.

![dieanalysis](./DIEanalysis.png)

이후 Ubuntu를 사용해 리눅스환경에서 프로그램을 실행하여 동작을 확인했습니다.

![Ubuntu](./initialrun.png)

### 2.2 Main Logic Finding
**Nice!** 성공 문자열을 Cross Reference (Xref) 하여 메인 로직이 위치한 함수를 찾았습니다.

![loop1](./loop1.png)
![loop2](./loop2.png)
![loop3](./loop3.png)

**input**으로 입력한 문자열이 총 세 번의 loop를 거쳐서 마지막 비교 문자열 s2와 비교되어
플래그를 출력하는것을 확인할 수 있었습니다.

input은 입력문자열이고 **loc_122B(input,rot)** -> **loc_1272(rot,result)** -> **loc_12B6(result2,result)** -> **memcmp(result2,s2,65)** 순서대로 진행됩니다.

input이 여러 암호화 loop들을 거쳐 s2와 비교되는것을 확인했습니다.
Nice를 출력하는 입력값을 알아내기 위해서 각 암호화 함수들을 분석했습니다.

### loc_122B Stack Frame & Register Setup
| Register / Memory | Variable Name (내 방식) | Description |

| `[rbp+var_4]` | `index` | Loop counter (initialized to 0) |

### Assembly Logic 
**Loop Condition:** Iterate 65 times 
```assembly
loc_122B:
    mov     eax, [rbp+var_4]           ; eax = index
    cdqe                               ; Convert Doubleword to Quadword
    lea     rdx, input                 ; rdx = input address
    movzx   eax, byte ptr [rax+rdx]    ; eax = input[index]
    add     eax, 0Dh                   ; eax = input[index] + 0xD
    and     eax, 7Fh                   ; eax = (input[index] + 0xD) & 0x7F
    mov     ecx, eax                   ; ecx = result
    mov     eax, [rbp+var_4]           ; eax = index
    cdqe                               ; Convert Doubleword to Quadword
    lea     rdx, rot                   ; rdx = rot address
    mov     [rax+rdx], cl              ; rot[index] = ecx
    add     [rbp+var_4], 1             ; index++

conclusion: rot[index]=(input[index]+0Dh)&7Fh
```

### loc_1272 Stack Frame & Register Setup
| Register / Memory | Variable Name (My Analysis) | Description |

| `[rbp+var_8]` | `index` | Loop counter (initialized to 0) |

### Assembly Logic 
**Loop Condition:** Iterate 65 times 
```assembly
loc_1272:
    mov     eax, 3Fh                   ; eax = 63
    sub     eax, [rbp+var_8]           ; eax = 63 - index
    cdqe                               ; Convert Doubleword to Quadword
    lea     rdx, rot                   ; rdx = rot address
    movzx   edx, byte ptr [rax+rdx]    ; edx = rot[63 - index]
    mov     eax, [rbp+var_8]           ; eax = index
    cdqe                               ; Convert Doubleword to Quadword
    lea     rcx, result                ; rcx = result address
    mov     [rax+rcx], dl              ; result[index] = rot[63 - index]
    add     [rbp+var_8], 1             ; index++

conclusion: result[index]=rot[63-index]
```

### loc_12B6 Stack Frame & Register Setup
| Register / Memory | Variable Name (My Analysis) | Description |

| `[rbp+var_C]` | `index` | Loop counter (initialized to 0) |

### Assembly Logic 
**Loop Condition:** Iterate 65 times 
```assembly
loc_12B6:
    mov     eax, [rbp+var_C]           ; eax = index
    cdqe                               ; Convert Doubleword to Quadword
    lea     rdx, result                ; rdx = result address
    movzx   eax, byte ptr [rax+rdx]    ; eax = result[index]
    mov     edx, [rbp+var_10]          ; edx = [rbp+var_10] (Key = 3)
    xor     eax, edx                   ; eax = result[index] ^ 3
    mov     ecx, eax                   ; ecx = result[index] ^ 3
    mov     eax, [rbp+var_C]           ; eax = index
    cdqe                               ; Convert Doubleword to Quadword
    lea     rdx, result2               ; rdx = result2 address
    mov     [rax+rdx], cl              ; result2[index] = result[index] ^ 3
    add     [rbp+var_C], 1             ; index++

conclusion: result2[index]=result[index]^3
```


## 3. Solution (풀이 과정)
암호화 순서를 분석하여 도출한 역방향 복호화 표입니다.
암호화와 반대로 복호화를하려면 함수실행 순서도 반대로 연산도 역연산으로 수행해야합니다.

| 순서 | 암호화 흐름 (Forward) | 연산 | $\leftrightarrow$ | 복호화 흐름 (Solver) | 역연산 수행 |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **1** | `loc_122B(input,rot)` | **ADD -> AND** | $\leftrightarrow$ | **Step 3** (마지막) | **AND -> SUB** |
| **2** | `loc_1272(rot,result)` | **String Reverse** | $\leftrightarrow$ | **Step 2** | **String Reverse** |
| **3** | `loc_12B6(result2,result)` | **XOR** | $\leftrightarrow$ | **Step 1** (시작) | **XOR** |

### Full Solver Code
[solution.c](./solution.c) 파일을 참고하세요.

## 4. Result
플래그 추출 성공: `DH{e615b75a4d563ac971466e05641d7aed556b62fcb460b6027f126bff411bfe63}`

![Success Screenshot](./flag_success.png)

## 5. Thoughts
처음에는 뭔가 대단한 함정이 있는줄 알고 pwndbg로 막 디버깅하다가 ida로 하나하나 뜯어보다가
아 그냥 단순한 역연산 문제구나 하고 어셈블리를 분석해서 역연산을 구현했다.
앞서 풀었던 simplecrackme2보다 쉬운건지 내 실력이 오른건지 모르겠는데 
좀 수월하게 풀었다. 같은 유형을 여러번 풀다보니 이제 단순 역연산 구현문제는 쉽게 느껴진다.




