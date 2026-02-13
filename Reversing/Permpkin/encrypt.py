with open('rev1.txt', 'r') as f:
    content = f.read()
with open('rev2.txt', 'r') as f:
    content2 = f.read()

decoded_text = "".join([chr(int(n)) for n in content.split()])
decoded_text1 = "".join([chr(int(n)) for n in content2.split()])
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
    for i in range(13):
        
        a1[0],a1[a4[i]]=a1[a4[i]],a1[0]
            
def sub_12E7(a1,a2):
    v4 = 13
    v3 = len(a1)
    if  v3 <= v4: 
        for i in range(v3):
            a1[i]=a1[i]^a2[i]
    else:
  
        for j in range(v4):
            a1[j] ^= a2[j]
        for k in range(v4,v3):
            a1[k] ^= a2[k % v4]
    
  
s=bytearray(b'_this_is_sample_flag_')
v8=bytearray(b'this_is_sample_flag')
v7=bytearray(b'CC2A750B63821F45AC20839')
v6=bytearray(32)


for i in range(23):
    v6[i]=sub_126E(v7[i]) # 여기까지는 맞음
    print(v6[i])
sub_11FD(s,0,len(s)-1,v6)  #sthisa_sl_fep_i_mlag_ 이게 나와야함

sub_12E7(s,v6) #tsbl|lWubTvoyXnUhcloY

print(s)
print(f"변환된 문자열: {decoded_text}")

sub_11FD(v8,0,len(v8)-1,v6)
sub_12E7(v8,v6)
print(v8)
print(f"변환된 문자열: {decoded_text1}")
