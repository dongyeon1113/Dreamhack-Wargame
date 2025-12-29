/*
    Problem: Dreamhack rev-basic-7
    Author: 강동연
    Date: 2025-12-29
    Description: 
        [암호화 로직 분석]
        1. 입력값의 각 문자를 (index & 7)만큼 ROL (Left Rotation) 수행
        2. 그 결과값을 index와 XOR 수행
        
        [복호화 로직 (Solver)]
        암호화의 역순으로 수행:
        1. 저장된 데이터와 index를 먼저 XOR (XOR의 역연산은 XOR)
        2. 그 결과값을 (index & 7)만큼 ROR (Right Rotation) 수행하여 원본 복구
*/

#include <stdio.h>

// ROR (Rotate Right) 구현 함수
// C언어에는 비트 회전 연산자가 없으므로 Shift(>>, <<)와 OR(|)를 조합해 직접 구현
unsigned char ROR(unsigned char value, int cnt)
{
    // 8비트 자료형이므로 8번 회전하면 제자리로 돌아옴 (따라서 8로 나눈 나머지만 수행)
    cnt = cnt % 8;

    /* [예시] 
       값: 1000 0011 (0x83), 1비트 오른쪽 회전 시
       
       1. value >> cnt : 0100 0001 (오른쪽으로 밀고, 왼쪽은 0으로 채움)
       2. value << (8-cnt) : 1000 0000 (밀려난 비트를 맨 앞으로 가져옴)
       3. OR 연산 (|)  : 1100 0001 (두 결과를 합침 -> 회전한것과 동일한 결과)
    */
    return (value >> cnt) | (value << (8 - cnt));
}

int main()
{
    // 기존의 데이터
    unsigned char data[] = {
        0x52, 0xDF, 0xB3, 0x60, 0xF1, 0x8B, 0x1C, 0xB5, 
        0x57, 0xD1, 0x9F, 0x38, 0x4B, 0x29, 0xD9, 0x26, 
        0x7F, 0xC9, 0xA3, 0xE9, 0x53, 0x18, 0x4F, 0xB8, 
        0x6A, 0xCB, 0x87, 0x58, 0x5B, 0x39, 0x1E
    };

    int len = sizeof(data);

    // 복호화 루프
    for (int i = 0; i < len; i++)
    {
        // 핵심 복호화 로직:
        // 암호화 순서: Input -> ROL -> XOR -> Data
        // 복호화 순서: Data -> XOR -> ROR -> Input (역순)
        
        // (data[i] ^ i) : 먼저 인덱스와 XOR 하여 1차 복구
        // ROR(..., i & 7) : 그 값을 다시 오른쪽으로 회전시켜 원본 문자 복구
        printf("%c", ROR((data[i] ^ i), i & 7));
    }
    
    return 0;
}
