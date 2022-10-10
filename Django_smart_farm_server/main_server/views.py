from http.client import HTTPResponse
from django.shortcuts import render

#서버
from datetime import datetime
import time
import socket
from .socket_server import sensor_log

# 서버 실행
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

# Create your views here.
def index(request):

    if request.method == 'GET' :
        return render(
            request,
            'main_server/index.html',
        )

    elif request.method == 'POST' :
        recv_sec = request.POST['recv_sec']
        save_hour = request.POST['save_hour']

        # 측정 간격, 저장 시간 확인
        print(recv_sec, save_hour)
        
        # 센서 로그 저장
        sensor_log(recv_sec,save_hour,client)

        return render(
            request,
            'main_server/index.html',
        )
    
   