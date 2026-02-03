with open("flag_out.txt", "rb") as f:
    flagdata = f.read()
with open("table.txt", "rb") as f:
    tabledata = f.read()

result = list()
decimal_table = list(tabledata) # 값(문자) -> 인덱스(0~63) 역참조용 리스트

# 인코딩된 데이터를 4글자씩 읽어 원본 3바이트로 복구
for i in range(0, len(flagdata), 4):
    chunk = list(flagdata[i : i+4])
    flag_chunk = "".join([chr(n) for n in chunk])
    
    # 패딩(=)이 있는 경우: 마지막 블록 처리
    if '=' in flag_chunk:
        # 테이블에서 각 글자의 인덱스(0~63) 추출
        idx1 = decimal_table.index(chunk[0])
        idx2 = decimal_table.index(chunk[1])
        # chunk[2]가 '='이면 에러가 날 수 있으므로 예외 처리가 필요할 수 있음 (현재 로직은 chunk[3]이 '='인 상황 가정)
        idx3 = decimal_table.index(chunk[2]) 
        
        # 1st Byte: idx1(6bit) << 2 | idx2 상위 2bit
        b1 = (idx1 << 2) | (idx2 >> 4)
        result.append(b1 & 0xFF)

        # 2nd Byte: idx2 하위 4bit | idx3 상위 4bit 
        b2 = ((idx2 & 0x0F) << 4) | (idx3 >> 2)
        result.append(b2 & 0xFF)
        
    # 패딩이 없는 경우: 꽉 찬 3바이트 블록 복구
    else:
        idx1 = decimal_table.index(chunk[0])
        idx2 = decimal_table.index(chunk[1])
        idx3 = decimal_table.index(chunk[2])
        idx4 = decimal_table.index(chunk[3])

        # 1st Byte 복구
        b1 = (idx1 << 2) | (idx2 >> 4)
        result.append(b1 & 0xFF)

        # 2nd Byte 복구 (idx2의 상위 비트 날리기 위해 & 0x0F)
        b2 = ((idx2 & 0x0F) << 4) | (idx3 >> 2)
        result.append(b2 & 0xFF)

        # 3rd Byte 복구 (idx3의 상위 비트 날리기 위해 & 0x03)
        b3 = ((idx3 & 0x03) << 6) | idx4
        result.append(b3 & 0xFF)
    
# 최종 플래그 출력
for i in range(len(result)):
    print(chr(result[i]), end='')
