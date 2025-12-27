/*
    Problem: Dreamhack rev-basic-5
    Author: 강동연
    Date: 2025-12-27
    Description: 마지막 input값이 NULL값인것을 고려한 연속적인 두 글자의 합 역연산 
        
*/
#include <stdio.h>
int main()
{
    // 데이터 영역에 있던 비교 값들
    unsigned char data[]={0xAD,0xD8,0xCB,0xCB,0x9D,0x97,0xCB,0xC4,0x92,0xA1,0xD2,0xD7,0xD2,0xD6,0xA8,0xA5,0xDC,0xC7,0xAD,0xA3,0xA1,0x98,0x4C};
    unsigned char input[23];
    int len=sizeof(data);
    
    
    for (int i=len-1; i>=0; i--)
    {
        //복원한 로직 적용
      if(i==len-1)
      {
        //마지막 input값이 NULL인것을 고려
        input[i]=data[i];
      } 
      else{
        //연속적인 두 글자를 더하는것의 역연산 적용
        input[i]=data[i]-input[i+1];
    }
  }
    for (int i=0; i<len; i++)
    {
      printf("%c",input[i]); //차례대로 출력
    }
}
