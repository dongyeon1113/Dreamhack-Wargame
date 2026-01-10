def solve():
    # 암호화된 파일 읽기 (바이너리 모드 rb)
    try:
        with open('secretMessage.enc', 'rb') as f_enc:
            enc_data = f_enc.read()
    except FileNotFoundError:
        print("파일이 없습니다.")
        return

    # 결과 담을 곳 준비
    raw_data = bytearray()

    # 디코딩 로직 시작
    temp = 0 # 이전 문자를 기억하는 변수
    i = 0    # 현재 위치 커서

    while i < len(enc_data):
        # [Case 1] 첫 번째 글자는 무조건 저장하고 시작
        if i == 0:
            temp = enc_data[i]
            raw_data.append(enc_data[i])
            i += 1 
        
        else:
            # [Case 2] 이전 문자와 현재 문자가 같으면? -> 압축된 구간
            # 예: aa0 패턴 발견 (temp=a, 현재=a)
            if enc_data[i] == temp:
                raw_data.append(temp)  # 현재 문자(두 번째 a) 저장
                
                # 바로 뒤에 있는 바이트(i+1)가 반복 횟수
                if i + 1 < len(enc_data):
                    count = enc_data[i+1] 
                    
                    # 횟수만큼 문자 추가 반복
                    for j in range(count):
                        raw_data.append(temp)
                
                # 중요: [현재 문자]와 [개수 숫자]를 모두 처리했으므로 2칸 점프
                i += 2 
            
            # [Case 3] 이전 문자와 다르면? -> 일반 문자
            # 예: b (앞의 a와 다름)
            else:
                raw_data.append(enc_data[i]) # 그냥 저장
                temp = enc_data[i]           # 이전문자 갱신
                i += 1                       # 1칸 전진

    # 결과 저장
    with open('secretMessage.raw', 'wb') as f_raw:
        f_raw.write(raw_data)
        

