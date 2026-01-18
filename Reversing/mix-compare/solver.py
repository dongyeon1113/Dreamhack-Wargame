
def checknot(data,i):
    # NOT(~) 연산의 역연산 수행 (Python의 정수 처리를 위해 0xFFFFFFFF 마스킹)
    # 원본: data = ~(input) + i
    return chr(~(data-i)& 0xFFFFFFFF)

def checkadd(data,i):
    # 덧셈의 역연산 -> 뺄셈
    # 원본: data = input + i
    return chr(data-i)

def checkdec(data,i):
    # 뺄셈의 역연산 -> 덧셈
    # 원본: data = input - i
    return chr(data+i)

def checkmul(data,i):
    # 곱셈의 역연산 -> 나눗셈 (몫)
    # 원본: data = input * i
    return chr(data//i)

def checkla(data,i):
    # 복합 연산의 역연산 (0x64를 빼고 i를 더함)
    # 원본: data = input + 0x64 - i
    return chr(data-0x64+i)


# 어셈블리어 분석을 통해 추출한 비교 값들
checknotarray=[0xFFFFFFAB,0XFFFFFFAF,0XFFFFFFD9,0XFFFFFFAD,0XFFFFFFAE,0XFFFFFFB0,0XFFFFFFB2,0XFFFFFFE0,0XFFFFFFE2,0XFFFFFFE1]
checkaddarray=[0x4F,0X53,0X4C,0X53,0X4F,0X57,0X83,0X54,0X59,0X87]
checkdecarray=[0x0C,0X13,0X3E,0X3B,0X3E,0X39,0X3A,0X38,0X0D,0X34]
checkmularray=[0x958,0x92E,0XA20,0X12F3,0XAF0,0X1452,0XB94,0X14B4,0XA56,0XB9A]
checklaarray=[0x63,0x5F,0X8F,0X59,0X8C,0X89,0X8C,0X55]


result="0d0c70a91ccd9b4f" # 앞부분 16바이트 (노가다로 찾은 값)

# checknot 구간 (16 ~ 25)
for i in range(10):
    result+=checknot(checknotarray[i],16+i)

# checkadd 구간 (26 ~ 35)
for i in range(10):
    result+=checkadd(checkaddarray[i],26+i)

# checkdec 구간 (36 ~ 45)
for i in range(10):
    result+=checkdec(checkdecarray[i],36+i)

# checkmul 구간 (46 ~ 55)
for i in range(10):
    result+=checkmul(checkmularray[i],46+i)

# checkla 구간 (인덱스 56 ~ 63)
for i in range(8):
    result+=checkla(checklaarray[i],56+i)

# 결과 출력
print(result)
