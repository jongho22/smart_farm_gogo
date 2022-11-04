from http.client import HTTPResponse
from django.shortcuts import render
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("클라이언트와 연결 되었습니다.")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print("연결이 해제 되었습니다.")


def on_subscribe(client, userdata, mid, granted_qos):
    print("연결 상태 : " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    print(str(msg.payload.decode("utf-8")))

client = mqtt.Client()
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect('broker.hivemq.com', 1883)
client.subscribe('test/send_data', 1)
client.loop_forever()

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
    
   