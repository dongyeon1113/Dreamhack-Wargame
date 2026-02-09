with open("key", "rb") as f:

    key_data = bytearray(f.read())


with open("flag.enc", "rb") as f:

    enc_data = bytearray(f.read())
with open("flag.enc", "rb") as f:

    flag_data = bytearray(f.read())



decrypted_data = bytearray(len(flag_data))



def ROR(val, n):

    max_bits = 16
   
    return ((val >> n) | (val << (16 - n))) & 0xFFFF

for i in range(0, len(flag_data),4):

    chunk = flag_data[i : i+2]  

    value = int.from_bytes(chunk, 'little')

    v3=value

    #print(hex(v3))

    chunk = flag_data[i+2 : i+4]  

    value = int.from_bytes(chunk, 'little')

    v4=value

    #print(hex(v4))

    for j in range(3):

        key_chunk = key_data[4*(2-j):4*(2-j)+2] #reverse order for decryption

        key1=int.from_bytes(key_chunk, 'little')

        #print(hex(key1))

        key_chunk = key_data[4*(2-j)+2:4*(2-j)+4]

        key2=int.from_bytes(key_chunk, 'little')

        #print(hex(key2))

       

        prev_v4=ROR(v3 ^ key2,7)
        temp=(v4^key1)&0xFFFF
        diff = (temp - prev_v4) & 0xFFFF
        prev_v3=ROR(diff,7)

        v3=prev_v3

        v4=prev_v4

       

    decrypted_data[i : i+2] = v3.to_bytes(2, 'little')

    decrypted_data[i+2 : i+4] = v4.to_bytes(2, 'little')

#print(decrypted_data)
for i in range(0, len(decrypted_data)):
    print(chr(decrypted_data[i]), end='')
