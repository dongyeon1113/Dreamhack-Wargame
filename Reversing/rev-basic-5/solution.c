/*
    Problem: Dreamhack rev-basic-5
    Author: 강동연
    Date: 2025-12-27
    Description: 
        문자열의 끝(NULL)을 이용한 역순(Backward) 복호화 알고리즘.
        (input[i] + input[i+1] = data[i] 관계식을 뒤에서부터 역산)
*/
#include <stdio.h>

int main()
{
    // 데이터 영역에 있던 비교 값들
    unsigned char data[] = {0xAD,0xD8,0xCB,0xCB,0x9D,0x97,0xCB,0xC4,0x92,0xA1,0xD2,0xD7,0xD2,0xD6,0xA8,0xA5,0xDC,0xC7,0xAD,0xA3,0xA1,0x98,0x4C};
    unsigned char input[23];
    int len = sizeof(data);
    
    // 뒤에서부터 앞으로 루프 (Backward Loop)
    for (int i = len - 1; i >= 0; i--)
    {
        if(i == len - 1)
        {
            // 마지막 글자는 NULL(0)과 더해졌으므로, data 값이 곧 input 값임
            input[i] = data[i];
        } 
        else {
            // 점화식 역산: input[i] = data[i] - input[i+1]
            input[i] = data[i] - input[i+1];
        }
    }

    for (int i = 0; i < len; i++)
    {
        printf("%c", input[i]); // 복구된 플래그 출력
    }
}
