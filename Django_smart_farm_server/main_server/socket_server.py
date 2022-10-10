import socket
import threading
from datetime import datetime
import time

under_text = "_"*50
server = socket.socket()
print('[소켓 생성완료]')
s_name = socket.gethostname()
print('서버 컴퓨터이름:', s_name)
server.bind(('203.252.240.64', 2578))
server.listen(3)
print('서버 리스닝...')

client, address = server.accept()
print(f"[클라이언트와 연결 되었습니다] => {address}\n{under_text}")

def sensor_log(log_recv_sec,n_hour) :
    now = datetime.now()
    temp_humi_string = ""
    start_time = time.time()
    start = time.time()
    start_time_save =f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}"

    while True:
        # 데이터 받음
        now = datetime.now()

        if time.time() - start_time >= log_recv_sec :
            
            data = client.recv(1024).decode()
            if not data :
                print(under_text+"\n클라이언트가 종료되었습니다.\n연결을 해제합니다.")
                break
            data = now.strftime("%H:%M:%S | ") + data
            
            temp_humi_string = temp_humi_string + data
            
            if time.time() - start >= n_hour :
                now = datetime.now()
                end_time_save = f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}"

                f = open(f'{start_time_save}_{end_time_save}.txt', 'a', encoding='utf-8')
                f.write(temp_humi_string)
                f.close()
                temp_humi_string = ""

                start_time_save =f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}"
                start = time.time()
                
            start_time = time.time()

            print('데이터 송신 받음 : ',data) #adderss

            # 클라이언트에 수신완료 전송
            client.send(bytes('데이터 전송 완료 : '+data[:-1], 'utf-8'))

#온습도 센서 로그 기록
sensor_log(10,30) # 왼쪽: 센서값 확인 간격(초)/ 오른쪽 파일 저장 간격(초)

client.close()