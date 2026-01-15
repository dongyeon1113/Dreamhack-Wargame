# Dreamhack: Public Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 2
- **Tool:** IDA Free, VS Code (Pyhon), Ubuntu, DIE
- **Description:** 암호화된 flag를 복호화하는 문제

## 2. Static Analysis (정적 분석)
### 2.1. Initial Analysis
제공된 public 파일에 확장자가 없어 파일 형식을 식별하기 위해 정적 분석 도구인 DIE (Detect It Easy) 를 사용했습니다. 분석 결과, 해당 파일이 리눅스 실행 파일(ELF 64-bit)임을 확인했습니다.

Reference: DIE는 실행 파일의 컴파일러, 패커, 파일 형식 등을 상세히 알려주는 도구입니다.

![dieanalysis](./DIEanalysis.png)

이후 Ubuntu를 사용해 리눅스환경에서 프로그램을 실행하여 동작을 확인했습니다.

 **Segmentation falut (core dumped)** 를 확인했습니다.


![Ubuntu](./initialrun.png)

다운로드 받은 폴더에는 public 리눅스 파일 뿐 아니라 **out.bin**파일과 **out.txt**파일이 있었습니다.

**out.bin**파일은 알 수 없는 문자들로 암호회되어 있는것을 볼 수 있었습니다.

![outbin](./outbin.png)

**out.txt**파일은 문제의 키가 될수도 있는 n1과 n2값을 알려줍니다.

![outtxt](./outtxt.png)


### 2.2 Main Logic Finding
**out.bin** 문자열을 Cross Reference (Xref) 하여 메인로직이 있는 함수를 찾았습니다.

**flag.txt**를 **rb**모드로 **fscanf**을 통해 받아오는것을 볼 수 있습니다. 

![IDAanalysis](./idaanalysis1.png)

**out.bin**을 **wb**모드로 **fopen**하는것을 확인할 수 있습니다.

"**flag.txt**에서 data를 받아와서 **암호화**과정을 거친다음에 **out.bin**파일에 **write**하는구나"라는 가성을 세웠습니다.
내가 해야할것은 암호화함수를 코드로 재구성한 다음에 복호화 코드를 짜야겠다고 생각했습니다.

![IDAanalysis](./idaanalysis2.png)

**call sub_1289**함수를 통해 나온 결과값을 **_fwrite**를 통해서 **out.bin**에 **write**하는것을 보고
**call sub_1289**이 암호화 함수라고 결론을 내렸습니다.

![IDAanalysis](./idaanalysis3.png)

**flag.txt**를 구하기 위해서는 암호화함수인 **sub_1289**뿐만이 아니라 주변 어셈블리들도 분석하여
역연산함수를 만들어야합니다.

**sub_1289**의 동작을 중심으로 분석했습니다.

### **main함수의 일부분** Stack Frame & Register Setup
| Register / Memory | Variable Name (내 방식) | Description |

| `[rbp+stream]` | `out.bin addr` | out.bin file address |

| `[rbp+var_174]` | `i` | loop counter |

| `[rbp+s]` | `flag.txt addr` | flag.txt file address |

| `[rbp+140]` | `n1` | n1 |

| `[rbp+138]` | `n2` | n2 |

### Assembly Logic 
```assembly

loc_1734:
    lea     rsi, aWb                    ; "wb"
    lea     rdi, aOutBin                ; "out.bin"
    call    _fopen                                
    mov     [rbp+stream], rax			;[rbp+stream]=out.bin addr
    mov     [rbp+var_174], 0			;index=0
    jmp     short loc_17CC
loc_17CC:
    mov     eax, [rbp+var_174]			;eax=index
    movsxd  rbx, eax					;rbx=index
    lea     rax, [rbp+s]				;rax=flag.txt addr
    mov     rdi, rax            		;rdi=flag.txt addr
    call    _strlen					    ;rax=strlen(flag)
    shr     rax, 2					    ;rax=strlen(flag)>>2
    cmp     rbx, rax					;if (index < strlen(flag)>>2) jmp loc_175A 
    jb      loc_175A

loc_175A:
    mov     eax, [rbp+var_174]			;eax=index
    cdqe
    lea     rdx, ds:0[rax*4]			;rdx=index*4
    lea     rax, [rbp+s]				;rax=flag.txt addr
    add     rax, rdx					
    mov     eax, [rax]					;eax=flag[4*i]
    mov     [rbp+var_16C], eax			;[rbp+var_16C]=flag[4*i]
    mov     eax, [rbp+var_16C]			;eax=flag[4*i]
    mov     rdx, [rbp+var_140]			;rdx=n1
    mov     rcx, [rbp+var_138]			;rcx=n2
    mov     rsi, rcx					;rsi=n2				
    mov     rdi, rax					;rdi=flag[4*i]
    call    sub_1289					;sub_1289(flag[4*i],n2,n1)
    mov     [rbp+ptr], rax				;[rbp+ptr]=(flag[4*i]^n2)mod n1
    mov     rdx, [rbp+stream]           ;rdx=out.bin addr
    lea     rax, [rbp+ptr]              ;rax=[rbp+ptr] addr
    mov     rcx, rdx                    ; s            
    mov     edx, 1                      ; n
    mov     esi, 8                      ; size
    mov     rdi, rax                    ; ptr
    call    _fwrite    
    add     [rbp+var_174], 1            ;index++

```

### **sub_1289** Stack Frame & Register Setup
| Register / Memory | Variable Name (내 방식) | Description |

| `[rbp+var_28]` | `n1` | modulo value |

| `[rbp+var_20]` | `n2` | exponent value |

| `[rbp+var_18]` | `flag[4*i]` | flag.txt 4byte chunk |

| `[rbp+var_10]` | `result` | return value |

| `[rbp+var_8]` | `cnt` | loop counter |

### Assembly Logic 
```assembly

    push    rbp
    mov     rbp, rsp
    sub     rsp, 30h                    
    mov     [rbp+var_18], rdi			;[rbp+var_18]=flag[4*i]
    mov     [rbp+var_20], rsi			;[rbp+var_20]=n2
    mov     [rbp+var_28], rdx			;[rbp+var_28]=n1
    cmp     [rbp+var_28], 0				;if (n1==0) jump loc_12B2
    jnz     short loc_12B2

loc_12B2:
    mov     [rbp+var_10], 1				;result=1
    mov     [rbp+var_8], 0				;cnt=0
    jmp     short loc_12EE

loc_12EE:
    mov     rax, [rbp+var_8]			;cnt=0
    cmp     rax, [rbp+var_20]			;if (cnt<n2) jump loc_12C4
    jb      short loc_12C4
    mov     rax, [rbp+var_10]			;retrun result
    leave
    retn
; } // starts at 1289
sub_1289 endp

loc_12C4:
    mov     rax, [rbp+var_10]			;rax=result
    imul    rax, [rbp+var_18]			;rax=result*flag[4*i]
    mov     [rbp+var_10], rax			;result=result*flag[4*i]
    cmp     [rbp+var_28], 0				;n1==0
    jz      short loc_12E9
    mov     rax, [rbp+var_10]			;rax=result
    mov     edx, 0					    ;edx=0
    div     [rbp+var_28]				;rax=result/n1, rdx=result%n1	
    mov     [rbp+var_10], rdx			;result=result%n1

loc_12E9:
    add     [rbp+var_8], 1				;cnt+=1

result=(flag[4*i]^n2)%n1
```


## Encoding Logic
flag.txt를 4byte씩 잘라서 **RSA**알고리즘을 적용

graph TD
    Node1["📃 Input: 원본 플래그 (String)"]
    Node2["⚙️ Process: 4바이트 단위 정수 변환 (Integer)"]
    Node3{"🔐 Encrypt: RSA 암호화 ( $Num \pow n2 \pmod{n1}$ )"}
    Node4["💾 Output: out.bin 파일 (Binary)"]

    Node1 -->|슬라이싱| Node2
    Node2 -->|계산| Node3
    Node3 -->|저장| Node4

    style Node3 stroke:#f00,stroke-width:2px,fill:#fff0f0

암호화 로직을 바탕으로 복호화 로직도 다이어그램으로 만들었습니다.

## Decoding Logic

### Example
Decoding `aa0bb1cc2df` back to `aabbbccccdf`:

```text
Input:     aa0        bb1        cc2        d      f
           └┬┘        └┬┘        └┬┘        |      |
Check:    Match      Match      Match      Raw    Raw
Action:   +0 char    +1 char    +2 chars    -      -
            ↓          ↓          ↓         ↓      ↓
Output:    aa         bbb        cccc       d      f
```

## 3. Solution (풀이 과정)
위 다이어그램을 바탕으로 solvercode를 짰습니다. 연속된 두 문자가 감지되면 바로 뒤에 오는 바이트가 추가 반복 횟수를 의미합니다.

[문자] == [이전 문자] → 압축 구간 해당 문자를 **다음 바이트 값**만큼 추가로 출력하고, 인덱스를 2칸 건너뜁니다.
그 외의 경우는 그대로 출력합니다.
예시:aa0 $\rightarrow$ aa (+0개 추가) bb1 $\rightarrow$ bbb (+1개 추가)

원본 파일을 복구하는 파이썬 코드는 다음과 같습니다.

### Full Solver Code
[solution](./solution.py) 파일을 참고하세요.

## 4. Result
![Success Screenshot](./flag_success.png)

## 5. Thoughts
암호화함수를 분석하고 복호화함수를 구현한다라는 전체적인 논리는 같지만 입력값이 아닌 raw, enc파일같이 
생소한 개념이 나오니 문제가 더 어렵게 느껴졌다. 게다가 flag가 출력되는 개념이 아니라 사진으로 띄어지는형식이어서
새로운 유형을 공부할 수 있어서 좋았다. 처음에 정적분석도 하지않고 pwndbg로 막 동적분석을 하다가 오히려 
더 꼬이는 느낌이어서 정적분석부터 천천히 하니 답을 찾을 수 있었다. 항상 기초부터 차근차근





