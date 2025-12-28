/*
    Problem: Dreamhack rev-basic-7
    Author: 강동연
    Date: 2025-12-29
    Description: 
        
*/
#include <stdio.h>
unsigned char ROR(unsigned char value, int cnt)
{//10000011 오른쪽으로 두 번 11100000 = 00100000 | 11000000
    cnt=cnt%8;
    return (value>>cnt | value<<(8-cnt));
}
int main()
{
    // 데이터 영역에 있던 비교 값들
    unsigned char data[] = {0x52,0xDF,0xB3,0x60,0xF1,0x8B,0x1C,0xB5,0x57,0xD1,0x9F,0x38,0x4B,0x29,0xD9,0x26,0x7F,0xC9,0xA3,0xE9,0x53,0x18,0x4F,0xB8,0x6A,0xCB,0x87,0x58,0x5B,0x39,0x1E};
    int len = sizeof(data);
    for (int i=0; i<len; i++)
    {
        printf("%c",ROR((data[i]^i),i&7));
    }
    

}
