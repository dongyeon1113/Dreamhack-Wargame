with open("flag_out.txt", "rb") as f:
            flagdata = f.read()
with open("table.txt", "rb") as f:
            tabledata = f.read()

result=list()
decimal_table = list(tabledata)




for i in range(0, len(flagdata), 4):
    chunk = list(flagdata[i : i+4])
    
    flag_chunk = "".join([chr(n) for n in chunk])
    
    b1=0
    b2=0
    b3=0
       
    if '=' in flag_chunk:
        idx1= decimal_table.index(chunk[0])
        idx2= decimal_table.index(chunk[1])
        idx3= decimal_table.index(chunk[2])
        b1 = (idx1<<2) | (idx2>>4)
        result.append(b1&0xFF)

        b2 = ((idx2&0x0F)<<4) | (idx3>>2)
        result.append(b2&0xFF)
    else:
        idx1= decimal_table.index(chunk[0])
        idx2= decimal_table.index(chunk[1])
        idx3= decimal_table.index(chunk[2])
        idx4= decimal_table.index(chunk[3])
        b1 = (idx1<<2) | (idx2>>4)
        result.append(b1&0xFF)

        b2 = ((idx2&0x0F)<<4) | (idx3>>2)
        result.append(b2&0xFF)

        b3 = (idx3&0x03)<<6 | idx4
        result.append(b3&0xFF)
    
for i in range(len(result)):
    print(chr(result[i]), end='')
