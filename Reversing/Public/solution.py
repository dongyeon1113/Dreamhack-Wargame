from Crypto.Util.number import inverse
import struct


n2 = 201326609       # 공개 지수 (e)
n1 = 4271010253    # 4271010253 = 65287 × 65419 n= pxq
phi =  65286*65418    #(p-1)(q-1)

#  복호화 키(d) 계산
d = inverse(n2, phi)

#  파일 읽기 및 복호화
flag_str = b""

with open('out.bin', 'rb') as f:
    while True:
        chunk = f.read(8)
        if not chunk: break
        
        # 암호문 숫자 로드 (out)
        enc_val = struct.unpack('<Q', chunk)[0]
        
        # RSA 복호화 (flag[4*i] = out^d % n1)
        dec_val = pow(enc_val, d, n1)
        
        # 숫자를 다시 4글자 문자열로 변환 (Little Endian)
        # 플래그 조각이 4바이트였으므로 4바이트로 변환
        flag_piece = struct.pack('<I', dec_val)
        
        flag_str += flag_piece

# 결과 출력
print("Found Flag:", flag_str)
