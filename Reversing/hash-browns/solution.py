import hashlib
import struct
import itertools
import string

def md5_brute_force(target_hash):
    # 사용할 문자셋: 소문자 + 숫자 + 특수문자 + 대문자
    charset = string.ascii_lowercase + string.digits + string.punctuation + string.ascii_uppercase
    
    # 1자리부터 4자리까지 조합 시도
    for length in range(1, 4):
        for guess in itertools.product(charset, repeat=length):
            password = ''.join(guess)
            # MD5 해시 생성
            guess_hash = hashlib.md5(password.encode('utf-8')).hexdigest()
            
            # 해시값 비교
            if guess_hash == target_hash:
                return password
    return None

part=[0xfe5d3a093968d02b,0xba0aa367c2862eae,
0x8BEA2ADA9E26604F,0x2E6F41C96DCF5224,
0x7FD91BD2949B75F3,0x5B1ED8E6072F3A6,
0xC94045C6D4887611,0x9D43DF6DF6B94D95,
0xB9A8A83C8AC08D80,0x6D78E80376518464,
0xE81A20F2023C2D0,0x2E41EAE69D89F186,
0x425C831DD2A3E5FD,0x82788DBBDC4100EC,
0x6D0FEE8D3901DD20,0xEBE82A0A41E5D783,
0x2AFA26414B72E506,0xD1848E9C21D114D] # MD5 해시값 쌍

result=""

for i in range(9):
    part1=part[i*2]
    part2=part[i*2+1]
    target_bytes = struct.pack('<Q', part1) + struct.pack('<Q', part2) # 리틀 엔디안으로 바이트 변환
    result += md5_brute_force(target_bytes.hex()) # brute-force 시도

print(result) # 최종 결과 출력
