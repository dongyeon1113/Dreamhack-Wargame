def solve_chunk_mapping():
    try:
        # 파일 로드 및 전처리 (줄바꿈, 패딩 제거)
        with open("text_in.txt", "rb") as f:
            text_in = f.read()
        with open("text_out.txt", "r") as f:
            text_out = f.read().replace('\n', '').replace('=', '')
    except FileNotFoundError:
        print("파일 없음")
        return

    table = [0] * 64
    
    # 3바이트(Plain) <-> 4글자(Encoded) 매핑 루프
    for i in range(0, len(text_in), 3):
        in_chunk = list(text_in[i : i+3])
        
        # 현재 청크에 해당하는 암호문 4글자 가져오기
        j = (i // 3) * 4
        out_chunk_vals = [ord(c) for c in text_out[j : j+4]]
        
        # 비트 연산으로 테이블 인덱스 역산 및 값 채우기
        if len(in_chunk) == 2: # 남은 데이터가 2바이트일 때
            table[in_chunk[0] >> 2] = out_chunk_vals[0]                                   # 1번째 글자
            table[(in_chunk[1] >> 4) | (16 * in_chunk[0]) & 0x30] = out_chunk_vals[1]   # 2번째 글자
            table[(4 * in_chunk[1]) & 0x3C] = out_chunk_vals[2]                         # 3번째 글자
            
        else: # 데이터가 3바이트 꽉 찼을 때
            table[in_chunk[0] >> 2] = out_chunk_vals[0]                                   # 1번째 글자
            table[(in_chunk[1] >> 4) | (16 * in_chunk[0]) & 0x30] = out_chunk_vals[1]   # 2번째 글자
            table[(in_chunk[2] >> 6) | (4 * in_chunk[1]) & 0x3C] = out_chunk_vals[2]    # 3번째 글자
            table[in_chunk[2] & 0x3F] = out_chunk_vals[3]                               # 4번째 글자

    # 복구된 테이블 저장
    with open("table.txt", "wb") as f:
        f.write(bytes(table))
    print("table.txt 생성 완료")

if __name__ == "__main__":
    solve_chunk_mapping()
