with open('flag1.txt', 'r') as f:
    content=f.read().strip().split()
    flag_data1 = bytearray(map(int,content))
with open('flag2.txt', 'r') as f:
    content=f.read().strip().split()
    flag_data2 = bytearray(map(int,content))


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
   
    for i in range(12, -1, -1):
        a1[0], a1[a4[i]] = a1[a4[i]], a1[0]
            
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
           
    
  

v7=bytearray(b'CC2A750B63821F45AC20839')
v6=bytearray(32)


for i in range(23):
    v6[i]=sub_126E(v7[i]) 

sub_12E7(flag_data1,v6)    

sub_11FD(flag_data1,0,len(flag_data1)-1,v6)  

print(flag_data1.decode())

sub_12E7(flag_data2,v6)    

sub_11FD(flag_data2,0,len(flag_data2)-1,v6)  

print(flag_data2.decode())

