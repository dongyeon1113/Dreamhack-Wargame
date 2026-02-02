def solve_chunk_mapping():
    
    
    
    try:
        with open("text_in.txt", "rb") as f:
            text_in = f.read()
        with open("text_out.txt", "r") as f:
            text_out = f.read().replace('\n', '').replace('=', '')
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return

    
    table = [0] * 64
    
    for i in range(0, len(text_in), 3):
        
        
        in_chunk = list(text_in[i : i+3])
        
        j = (i // 3) * 4
        out_chunk_chars = text_out[j : j+4]
       
        
        out_chunk_vals = []
        for char in out_chunk_chars:
            
            char=ord(char)
            out_chunk_vals.append(char)
        
       
        
        if len(in_chunk) == 2:
            
            table[in_chunk[0]>>2]=out_chunk_vals[0] 
            table[(in_chunk[1]>>4) | (16*in_chunk[0]) & 0x30]=out_chunk_vals[1]  
            table[(4*in_chunk[1])&0x3C]=out_chunk_vals[2]
            
        else:
            
            table[in_chunk[0]>>2]=out_chunk_vals[0]
            table[(in_chunk[1]>>4) | (16*in_chunk[0]) & 0x30]=out_chunk_vals[1]  
            table[(in_chunk[2]>>6) | (4*in_chunk[1]) & 0x3C]=out_chunk_vals[2]
            table[in_chunk[2] & 0x3F]=out_chunk_vals[3]      
        

   
    print(table)
    with open("table.txt", "wb") as f:
        f.write(bytes(table))
    print("✅ table.txt 생성 완료")

if __name__ == "__main__":
    solve_chunk_mapping()
