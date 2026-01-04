/*
    Problem: Dreamhack simple_crack_me_2
    Author: 강동연
    Date: 2025-01-04
    Description: 
        [암호화 로직 분석]
        1. 4011EF (XOR) -> Key: unk_402068
        2. 401263 (ADD) -> Val: 31
        3. 4012B0 (SUB) -> Val: 90
        4. 4011EF (XOR) -> Key: unk_40206D
        5. 4012B0 (SUB) -> Val: 77
        6. 401263 (ADD) -> Val: 243
        7. 4011EF (XOR) -> Key: unk_402072
        
        [복호화 로직 (Solver)]
        - 암호화의 역순으로 수행해야 함 
        - 각 연산의 역연산을 수행 (Add <-> Sub, XOR <-> XOR)
*/

#include <stdio.h>

// [복호화 함수 1] XOR 연산
// 특징: XOR은 역연산도 XOR이다. ((A ^ B) ^ B = A)
// 암호화된 문자열을 Key값과 XOR하여 원래 값으로 복구
void solve_4011EF(unsigned char *s2, unsigned char *unk, int s2_len, int unk_len)
{
    for(int i=0; i<s2_len; i++)
    {
        // 암호문[i] = 키[i] ^ 암호문[i]
        s2[i] = unk[i % unk_len] ^ s2[i];
    }
}

// [복호화 함수 2] 뺄셈 연산 
// 원본 코드의 더하기 연산을 상쇄하기 위해 값을 뺌
void solve_401263(unsigned char *s2, int num, int s2_len)
{
    for(int i=0; i<s2_len; i++)
    {
        s2[i] = s2[i] - num;
    }
}

// [복호화 함수 3] 덧셈 연산 
// 원본 코드의 빼기 연산을 상쇄하기 위해 값을 더함
void solve_4012B0(unsigned char *s2, int num, int s2_len)
{
    for(int i=0; i<s2_len; i++)
    {
        s2[i] = s2[i] + num;
    }
}

int main()
{

    // 최종 비교되는 암호화된 문자열 
    unsigned char s2[] = {
        0xF8, 0xE0, 0xE6, 0x9E, 0x7F, 0x32, 0x68, 0x31, 
        0x05, 0xDC, 0xA1, 0xAA, 0xAA, 0x09, 0xB3, 0xD8, 
        0x41, 0xF0, 0x36, 0x8C, 0xCE, 0xC7, 0xAC, 0x66, 
        0x91, 0x4C, 0x32, 0xFF, 0x05, 0xE0, 0xD9, 0x91
    };

    // 암호화 과정에서 사용된 키 값들
    unsigned char unk_402068[] = { 0xDE, 0xAD, 0xBE, 0xEF };
    unsigned char unk_40206D[] = { 0xEF, 0XBE, 0XAD, 0XDE };
    unsigned char unk_402072[] = { 0x11, 0x33, 0x55, 0x77, 0x99, 0xBB, 0xDD };

    // 배열 길이 계산
    int len = sizeof(s2);
   
    // [역연산 시작]
    // 암호화 순서의 정반대로 진행

   
    // 원본: 4011EF(..., unk_402072) XOR -> XOR
    solve_4011EF(s2, unk_402072, len, sizeof(unk_402072));

    // 원본: 401263(..., 243) SUB -> ADD 
    solve_401263(s2, 243, len); // 역연산: SUB

    // 원본: 4012B0(..., 77) ADD -> SUB
    solve_4012B0(s2, 77, len);  // 역연산: ADD

    // 원본: 4011EF(..., unk_40206D) XOR -> XOR
    solve_4011EF(s2, unk_40206D, len, sizeof(unk_40206D));

    // 원본: 4012B0(..., 90) ADD -> SUB
    solve_4012B0(s2, 90, len);  // 역연산: ADD

    // 원본: 401263(..., 31) SUB -> ADD
    solve_401263(s2, 31, len);  // 역연산: SUB

    // 원본: 4011EF(..., unk_402068) SUB -> XOR
    solve_4011EF(s2, unk_402068, len, sizeof(unk_402068));
    
    // 복호화가 완료된 flag 출력
    for (int i=0; i<len; i++)
    {
        printf("%c", s2[i]);
    }

    
    return 0;
}
