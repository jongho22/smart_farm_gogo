from socket import *
import threading
from datetime import datetime
import time

list=[]

under_text = "_"*50
server = socket(AF_INET, SOCK_STREAM)
print('[소켓 생성완료]')
s_name = "test" 
#socket.gethostname()
print('서버 컴퓨터이름:', s_name)
server.bind(('203.252.240.64', 2578))
server.listen(3)
print('서버 리스닝...')

client, address = server.accept()
print(f"[클라이언트와 연결 되었습니다] => {address}\n{under_text}")

def sensor_log(log_recv_sec) :

    start_time = time.time()

    while True:
        # 데이터 받음
        now = datetime.now()

        if time.time() - start_time >= log_recv_sec :
            #f = open(f'test.txt', 'a', encoding='utf-8')
            data = client.recv(1024).decode()
            if not data :
                print(under_text+"\n클라이언트가 종료되었습니다.\n연결을 해제합니다.")
                break
            data = now.strftime("%H:%M:%S | ") + data
            #f.write(data)
            #f.close()
            start_time = time.time()

            print('데이터 송신 받음 : ',data) #adderss

            # 클라이언트에 수신완료 전송
            client.send(bytes('데이터 전송 완료 : '+data[:-1], 'utf-8'))

#온습도 센서 로그 기록
sensor_log(10)

client.close()