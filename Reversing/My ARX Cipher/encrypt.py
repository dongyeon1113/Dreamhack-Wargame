with open("key", "rb") as f:
    key_data = bytearray(f.read())  # 키 파일 로드

with open("flag.enc", "rb") as f:
    flag_data = bytearray(f.read()) # 암호화할 데이터 로드

# 4바이트 블록 단위 처리
for i in range(0, len(flag_data), 4):
    v3 = int.from_bytes(flag_data[i : i+2], 'little')   # 앞 2바이트 정수화
    v4 = int.from_bytes(flag_data[i+2 : i+4], 'little') # 뒤 2바이트 정수화
    
    # 3라운드 암호화 연산
    for j in range(3):
        key1 = int.from_bytes(key_data[4*j : 4*j+2], 'little')
        key2 = int.from_bytes(key_data[4*j+2 : 4*j+4], 'little')
        
        # v3를 7비트 왼쪽 순환 이동(ROL) 후 연산
        v5 = key1 ^ (v4 + ((v3 << 7) | (v3 >> 9)))
        # v4를 7비트 왼쪽 순환 이동(ROL) 후 연산
        v3 = (key2 ^ ((v4 << 7) | (v4 >> 9))) & 0xFFFF
        v4 = v5 & 0xFFFF # 결과 업데이트
        
    # 암호화된 값 다시 바이트로 저장
    flag_data[i : i+2] = v3.to_bytes(2, 'little')
    flag_data[i+2 : i+4] = v4.to_bytes(2, 'little')

print(flag_data) # 최종 결과 출력
