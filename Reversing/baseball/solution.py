def solve_chunk_mapping():
    # 1. Base64 색인표 (문제에서 주어진 순서대로)
    B64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    # 2. 파일 읽기
    try:
        with open("text_in.txt", "rb") as f:
            text_in = f.read()
        with open("text_out.txt", "r") as f:
            text_out = f.read().replace('\n', '').replace('=', '') # 줄바꿈/패딩 제거
    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")
        return

    # 3. 테이블 배열 준비 (결과 저장용)
    # 어떤 로직으로 매핑할지에 따라 크기가 달라질 수 있으나, 일단 256으로 둡니다.
    table = [0] * 256
    
    # 4. 루프: 입력은 3바이트씩, 출력은 4글자씩 건너뜀
    # range(시작, 끝, 스텝)
    for i in range(0, len(text_in), 3):
        
        # [A] 입력 데이터 3바이트 가져오기 (List Slicing)
        # 예: [65, 66, 67] ('A', 'B', 'C')
        in_chunk = list(text_in[i : i+3])
        
        # [B] 출력 데이터 4글자 가져오기
        # 입력 인덱스 i가 0, 3, 6... 갈 때, 출력 인덱스 j는 0, 4, 8... 로 가야 함
        j = (i // 3) * 4
        out_chunk_chars = text_out[j : j+4]

        # 짝이 안 맞으면(마지막 부분 등) 처리 중단
        if len(out_chunk_chars) < 4:
            break

        # [C] 출력 글자를 10진수(색인값)로 변환 (0~63)
        # 예: 'A' -> 0, 'z' -> 51 ...
        out_chunk_vals = []
        for char in out_chunk_chars:
            if char in B64_CHARS:
                out_chunk_vals.append(B64_CHARS.index(char))
            else:
                out_chunk_vals.append(0) # 예외 처리

        # -----------------------------------------------------------
        # ⭐ 여기가 말씀하신 "연산"을 수행하는 부분입니다.
        # 현재 변수 상태:
        # in_chunk       = [Byte1, Byte2, Byte3]  (예: [65, 66, 67])
        # out_chunk_vals = [Val1, Val2, Val3, Val4] (예: [10, 22, 5, 41])
        # -----------------------------------------------------------

        
        if len(in_chunk) == 2:
            table[in_chunk[0]>>2]=out_chunk_vals[0] # 첫 번째 바이트 -> 첫 번째 결과값
            table[(in_chunk[1]>>4) | (16*in_chunk[0]) & 0x30]=out_chunk_vals[1]  
            table[(in_chunk[2]>>6) | (4*in_chunk[1]) & 0x3C]=out_chunk_vals[2]
        else:
            table[in_chunk[0]>>2]=out_chunk_vals[0]
            table[(in_chunk[1]>>4) | (16*in_chunk[0]) & 0x30]=out_chunk_vals[1]  
            table[(in_chunk[2]>>6) | (4*in_chunk[1]) & 0x3C]=out_chunk_vals[2]
            table[in_chunk[2] & 0x3F]=out_chunk_vals[3]      
        # (네 번째 값 out_chunk_vals[3]은 짝이 없어서 남게 됩니다)

    # 5. 결과 파일 저장
    print(table)
    with open("table.txt", "wb") as f:
        f.write(bytes(table))
    print("✅ table.txt 생성 완료")

if __name__ == "__main__":
    solve_chunk_mapping()
