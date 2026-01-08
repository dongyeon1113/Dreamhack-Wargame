/*
    Problem: Dreamhack r-xor-t
    Author: 강동연
    Date: 2025-01-08
    Description: 
        [암호화 로직 분석]
        1. loc_122B(input,rot) (ADD -> XOR) -> rot[i]=(input[i] + 0Dh) & 7Fh 
        2. loc_1272(rot,result) (REVERSE) -> result[i]=rot[63-i] 
        3. loc_12B6(result2,result) (XOR) -> result2[i]=result[i] ^ 3 
       
        
        [복호화 로직 (Solver)]
        - 암호화의 역순으로 수행해야 함 
        - 각 연산의 역연산을 수행 (Add <-> Sub, XOR <-> XOR)
*/

#include <stdio.h>

// [복호화 함수 1] XOR 연산
// 특징: XOR은 역연산도 XOR이다. ((A ^ B) ^ B = A)
// 최종문자열 s2를 3과 XOR하여 result에 저장
void solve_loc_12B6(unsigned char *s2, unsigned char *result, int s2_len)
{
    for(int i=0; i<s2_len; i++)
    {
        
        result[i] = s2[i] ^ 3;
    }
}

// [복호화 함수 2] Reverse
// 원본 코드인 문자열 뒤집기를 상쇄시키기 위해서 다시 뒤집어서 rot에 저장
void solve_loc_1272(unsigned char *result, unsigned char *rot, int result_len)
{
    for(int i=0; i<result_len; i++)
    {
        rot[i]=result[63-i];
    }
}

// [복호화 함수 3] AND연산 후 SUB연산
// 원본 코드의 AND 연산을 상쇄하기 위해 AND연산 다시 시행 후 ADD의 역연산 SUB 수행
void solve_loc_122B(unsigned char *rot, unsigned char *input, int rot_len)
{
    for(int i=0; i<rot_len; i++)
    {
        input[i] = (rot[i] & 127) - 13;
    }
}

int main()
{

    // 최종 비교되는 암호화된 문자열 
    unsigned char s2[] = "C@qpl==Bppl@<=pG<>@l>@Blsp<@l@AArqmGr=B@A>q@@B=GEsmC@ArBmAGlA=@q";
    unsigned char result[100]={0};
    unsigned char rot[100]={0};
    unsigned char input[100]={0};

    // 배열 길이 계산
    int len = sizeof(s2);
   
    // [역연산 시작]
    // 암호화 순서의 정반대로 진행
    solve_loc_12B6(s2, result, len);

   
    solve_loc_1272(result, rot, len); 

   
    solve_loc_122B(rot, input, len);  


    // 복호화가 완료된 flag 출력
    for (int i=0; i<len; i++)
    {
        printf("%c", input[i]);
    }

    
    return 0;
}
