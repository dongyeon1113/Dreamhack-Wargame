# Dreamhack: simple-operation Write-up

## 1. Problem Overview
- **Category:** Reversing
- **Difficulty:** Level 1
- **Tool:** IDA Free, VS Code (C Language), Ubuntu 24.04.1 LTS
- **Description:** 랜덤으로 입력되는 값과 사용자의 입력을 xor 연산하여 기존에 준비되어있는 string과 비교하는 문제

## 2. Static Analysis (정적 분석)
### 2.1. Main Logic Finding
`Congrats!` 문자열을 Xref하여 메인함수를 찾았습니다.
해당 함수를 분석한 결과, 우선 get_rand_num함수를 통해 16진수 수를 받아와 10진수로 입력받은 수와 xor연산을 합니다.
그 결과를 snprintf함수를 사용해 s문자열에 저장하는것을 볼 수 있습니다.

![IDA Graph View](./analysis1.png)

아래 Graph View를 보면 cmp [rbp+var4], 7를 통해서 rbp+var4가 index이고 loop count가 7회인 반복문을 시행하고있다는것을 알 수 있습니다.
loc_143E에서는 복잡해보이지만 rbp+var4가 반복문의 index인것을 안다면 단순히 s1[index]=s[7-index]연산을 수행하고 있습니다.
7번의 반복문이 끝나게 되면 기존에 준비되어있던 비교 문자열 "a0b4c1d7"과 strncmp함수를 통해 비교합니다.

![IDA Graph View](./analysis2.png)


### 2.2. Assembly to C Reconstruction (핵심)
분석한 어셈블리 코드를 바탕으로 C언어 의사 코드(Pseudo-code)로 복원했습니다. 핵심 로직은 **입력 문자를 (i & 7)만큼 ROL 회전시킨 후, 인덱스(i)와 XOR 연산하여 비교**하는 과정입니다.

**[Assembly Code]**
```assembly
mov     eax, [rsp+18h+var_18]   ; i (index) 값을 가져옴
and     eax, 7                  ; i & 7 (회전 횟수 계산)
movsxd  rcx, [rsp+18h+var_18]
mov     [rsp+18h+var_10], rcx   ; (메모리 정리 과정)
mov     rdx, [rsp+18h+arg_0]    ; 입력값 배열 주소
movzx   ecx, al                 ; ecx = 회전 횟수 (i & 7)
mov     rax, [rsp+18h+var_10]
movzx   eax, byte ptr [rdx+rax] ; eax = input[i] (1바이트 로드)
rol     al, cl                  ; ROL (Rotate Left) al, cl
movzx   eax, al
xor     eax, [rsp+18h+var_18]   ; Result ^ i (XOR)
lea     rdx, unk_140003000      ; 비교할 데이터(data) 주소 로드
cmp     eax, ecx                ; 최종 비교 (Compare)
```

**[Reconstructed C Code]**
```c

#include <stdbool.h> // bool, true, false 사용을 위해

// ROL (Rotate Left) 함수 구현
// C언어에는 비트 회전 연산자가 없으므로 Shift(<<, >>)와 OR(|)를 조합해 구현
unsigned char ROL(unsigned char value, int cnt)
{
    // 8비트 자료형이므로 8번 회전하면 제자리로 돌아옴
    cnt = cnt % 8;

    /* [구현 예시] 
       값: 1000 0011 (0x83), 1비트 왼쪽 회전 시 (ROL 1)
       
       1. value << cnt      : 0000 0110 (왼쪽으로 밀고, 오른쪽은 0으로 채움)
       2. value >> (8-cnt)  : 0000 0001 (밀려난 최상위 비트가 맨 뒤로 이동)
       3. OR 연산 (|)       : 0000 0111 (두 결과를 합침 -> 회전 완료)
    */
    return (value << cnt) | (value >> (8 - cnt));
}

bool check(char* input, char* data, int len)
{
 
    for (int i = 0; i < len; i++)
    {
        // [검증 로직]
        // 1. 입력 문자(input[i])를 (i & 7)만큼 왼쪽으로 회전 (ROL)
        // 2. 그 결과를 인덱스(i)와 XOR 연산
        // 3. 미리 정의된 데이터(data[i])와 비교
        if ( (ROL(input[i], i & 7) ^ i) != data[i] )
        {
            return false; // 하나라도 다르면 검증 실패
        }
    }

    return true; // 모든 검증 통과
}
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


