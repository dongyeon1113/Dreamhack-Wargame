# Dreamhack: rev-basic-5 Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 2
- **Tool:** IDA Free, VS Code (C Language)
- **Description:** 사용자 입력의 연속된 두 글자 합을 검증하는 로직을 분석하고, 문자열 끝(NULL)을 기점으로 역순 계산하여 플래그를 복구함

## 2. Static Analysis (정적 분석)
### 2.1. Main Logic Finding
`Correct` 문자열을 Xref하여 메인 검증 함수(`sub_140001000`)를 찾았습니다.
함수 내부는 반복문을 돌며 사용자 입력값의 각 문자를 변환하고 연산하며 기존의 데이터와 비교하고있습니다.

![IDA Graph View](./analysis.png)


### 2.2. Assembly to C Reconstruction (핵심)
어셈블리 코드를 분석하여 C언어로 복원했습니다.
- 인접한 두 문자의 합(input[i] + input[i+1])을 기존에 가지고있는 data[i]와 비교하여 검증하는 로직을 식별했습니다.
- 문자열 끝이 **NULL(0)**임을 이용해, 마지막 글자부터 역순으로 추론하는 Backward Solver를 구현하여 해결했습니다.

**[Assembly Code]**
```assembly
movsxd  rax, [rsp+18h+var_18]
mov     rcx, [rsp+18h+arg_0]
movzx   eax, byte ptr [rcx+rax]
mov     ecx, [rsp+18h+var_18]
inc     ecx
movsxd  rcx, ecx
mov     rdx, [rsp+18h+arg_0]
movzx   ecx, byte ptr [rdx+rcx]
add     eax, ecx
movsxd  rcx, [rsp+18h+var_18]
lea     rdx, unk_140003000
movzx   ecx, byte ptr [rdx+rcx]
cmp     eax, ecx
```

**[Reconstructed C Code]**
```c
// 제가 복원한 로직입니다.
Bool check(char* input,char* data)
{
  for (int i=0; i<23; i++)
    {
      if ((input[i]+input[i+1])==data[i])// 인접한 두 문자의 합을 기존의 데이터와 한 글자씩 비교
        {
            continue;
        }
      else
        {
            return False;
        }
    }
  return True;
}
```

## 3. Solution (풀이 과정)


### Full Solver Code
[solution.c](./solution.c) 파일을 참고하세요.

## 4. Result
플래그 추출 성공: 

![Success Screenshot](./flag_success.png)
