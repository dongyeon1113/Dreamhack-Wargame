with open('rev1.txt', 'r') as f:
    content = f.read()

# 2. 공백을 기준으로 숫자 분리 및 문자로 변환
# chr() 함수는 10진수 아스키 값을 문자로 바꿔줍니다.
decoded_text = "".join([chr(int(n)) for n in content.split()])
def sub_126E(a1):
    v2=0
    if a1 >=0x30 and a1 <=0x39:
        return a1 - 40
    elif a1 >0x45:
        if a1>0x4F:
            if a1<=0x59:
                return a1 - 80
        else:
            return a1-70
    else:
        return a1-60
    return v2
def swap(x, y):
    return y, x
def sub_11FD(a1,a2,a3,a4):
    result=0
    for i in range(23):
        print(a1.decode())
        a1[0],a1[a4[i]]=a1[a4[i]],a1[0]
        print(a1.decode())      
def sub_12E7(a1,a2):
    for i in range(len(a1)):
        a1[i]=a1[i]^a2[i]   
s=bytearray(b'_this_is_sample_flag_')
v8=bytearray(b'this_is_sample_flag')
v7=bytearray(b'CC2A750B63821F45AC20839')
v6=bytearray(32)


for i in range(23):
    v6[i]=sub_126E(v7[i]) # 여기까지는 맞음

sub_11FD(s,0,len(s)-1,v6)

sub_12E7(s,v6)

print(s)
print(f"변환된 문자열: {decoded_text}")
