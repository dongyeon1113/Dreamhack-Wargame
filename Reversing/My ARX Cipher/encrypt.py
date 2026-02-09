with open("key", "rb") as f:
    key_data = bytearray(f.read())

with open("flag.enc", "rb") as f:
    flag_data = bytearray(f.read())
for i in range(0, len(flag_data)):
    print(hex(flag_data[i]), end=' ')
with open("output", "rb") as f:
    output_data = bytearray(f.read())
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
        key_chunk = key_data[4*j:4*j+2]
        key1=int.from_bytes(key_chunk, 'little')
        #print(hex(key1))
        key_chunk = key_data[4*j+2:4*j+4]
        key2=int.from_bytes(key_chunk, 'little')
        #print(hex(key2))
        v5 = key1 ^ (v4 + ((v3 << 7) | (v3 >> 9)))
        v3 = (key2 ^ ((v4 << 7) | (v4 >> 9)))& 0xFFFF
        
        v4 = v5& 0xFFFF
    flag_data[i : i+2] = v3.to_bytes(2, 'little')
    flag_data[i+2 : i+4] = v4.to_bytes(2, 'little')

