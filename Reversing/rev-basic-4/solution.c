/*
    Problem: Dreamhack rev-basic-4
    Author: 강동연
    Date: 2025-12-26
    Description: 
        IDA Analysis를 통해 ROL 연산을 식별하고 역산 스크립트를 작성함.
        Nibble Swap 구조라 역산 로직이 정방향 로직과 동일함.
*/
#include <stdio.h>
int main()
{
    // 데이터 영역에 있던 비교 값들
    unsigned char data[]={0x24,0x27,0x13,0xC6,0xC6,0x13,0x16,0xE6,0x47,0xF5,0x26,0x96,0x47,0xF5,0x46,0x27,0x13,0x26,0x26,0xC6,0x56,0xF5,0xC3,0xC3,0xF5,0xE3,0xE3};
    int len=sizeof(data);
    for (int i=0; i<len; i++)
    {
        //복원한 로직 적용
        printf("%c",((data[i]>>4) | (data[i]<<4)));
    }
    
}
