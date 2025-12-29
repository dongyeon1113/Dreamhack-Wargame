# Dreamhack: rev-basic-7 Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 2
- **Tool:** IDA Free, VS Code (C Language)
- **Description:** 사용자 입력값에 대해 비트 회전(ROL) 및 XOR 연산을 수행한 뒤, 메모리에 하드코딩된 데이터와 일치하는지 검증하는 로직을 분석하고 역연산 스크립트를 작성하는 문제

## 2. Static Analysis (정적 분석)
### 2.1. Main Logic Finding
`Correct` 문자열을 Xref하여 메인 검증 함수(`sub_140001000`)를 찾았습니다.
해당 함수를 분석한 결과, 반복문을 순회하며 아래와 같은 검증 로직을 수행하는 것을 파악했습니다.

- Rotate Count 계산: 인덱스(i)와 7을 AND 연산하여 회전 횟수를 구함.
- ROL (Rotate Left): 입력받은 문자를 위에서 구한 횟수만큼 왼쪽으로 회전.
- XOR: 회전된 결과값을 다시 인덱스(i)와 XOR 연산.
- Compare: 최종 연산 결과가 데이터 영역(data)에 저장된 값과 일치하는지 비교.

![IDA Graph View](./analysis.png)


### 2.2. Assembly to C Reconstruction (핵심)
어셈블리 코드를 분석하여 C언어로 복원했습니다.
- 우선 인덱스와 7을 AND연산 하여 회전횟수를 구합니다.
- 그 결과값을 입력받은 문자와 ROL연산을 수행한 후 XOR 연산하여 data와 비교합니다.

**[Assembly Code]**
```assembly
mov     eax, [rsp+18h+var_18]
and     eax, 7
movsxd  rcx, [rsp+18h+var_18]
mov     [rsp+18h+var_10], rcx
mov     rdx, [rsp+18h+arg_0]
movzx   ecx, al
mov     rax, [rsp+18h+var_10]
movzx   eax, byte ptr [rdx+rax]
rol     al, cl
movzx   eax, al
xor     eax, [rsp+18h+var_18]
movsxd  rcx, [rsp+18h+var_18]
lea     rdx, unk_140003000
movzx   ecx, byte ptr [rdx+rcx]
cmp     eax, ecx
```

**[Reconstructed C Code]**
```c

// ROL (Rotate Left) 구현 함수
// C언어에는 비트 회전 연산자가 없으므로 Shift(>>, <<)와 OR(|)를 조합해 직접 구현
unsigned char ROL(unsigned char value, int cnt)
{
    //8비트 자료형이므로 8번 회전하면 제자리로 돌아옴 (따라서 8로 나눈 나머지만 수행)
    cnt=cnt%8;
    /* [예시] 
       값: 1000 0011 (0x83), 1비트 왼쪽으로 회전 시
       
       1. value << cnt : 0000 0110 (왼쪽으로 한 칸 밀어버림)
       2. value >> (8-cnt) : 0000 0001 (오른쪽으로 일곱 칸 밀어버림)
       3. OR 연산 (|)  : 0000 0111 (두 결과를 or연산하여 합침 -> 마치 회전한것과 동일한 결과)
    */
    return (value << cnt) | (value >> (8 - cnt));
}
Bool check(char* input, char* data)
{
    int len=sizeof(data);
    for (int i = 0; i < len; i++)
    {
        // [검증 로직]
        // 입력글자를 인덱스 & 7 만큼 ROL연산 한 후 다시 index와 xor연산 한 후 data와 비교
        if ((ROL(input[i],(i&7))^i) == data[i])
        {
            continue;
        }
        else
        {
            return False; // 검증 실패
        }
    }

    return True; // 모든 조건 통과
}
```

## 3. Solution (풀이 과정)
**[분석표]** 를 참고하면 **인접한 두 문자의 합(input[i] + input[i+1])** 을 데이터 배열과 비교하는 방식인것을 알 수 있습니다. 정방향 연산으로는 값을 확정할 수 없어서 모든 C 문자열의 끝은 **NULL(0)** 로 끝난다는 점에 착안하여 **역연산**을 설계했습니다.
가장 마지막 문자는 input[22] + 0 = data[22]가 성립하므로, 배열의 끝에서부터 시작하여 앞쪽으로 이동하는 역추적(Backtracking) 방식을 사용했습니다. input[i] = data[i] - input[i+1] 공식을 통해 문자열을 순차적으로 복원하여 플래그를 획득할 수 있었습니다.

### Full Solver Code
[solution.c](./solution.c) 파일을 참고하세요.

## 4. Result
플래그 추출 성공: `DH{All_l1fe_3nds_w1th_NULL}`

![Success Screenshot](./flag_success.png)

## 5. 느낀점
난이도가 하나 올라갔다고 같은유형이어도 깊이가 달라진것같다. 
가장기초적인 C언어 문자열의 끝은 NULL값이라는것을 파악하는것이 오래걸렸고, 그 뒤로 역연산을 구현하는것은 할만했다. 
어렵게 생각하지말고 쉽게 생각하자 가끔은 단순함이 답일때도있다.

