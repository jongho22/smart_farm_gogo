from pickle import TRUE
import paho.mqtt.client as mqtt
import json
import time
from serial import Serial
import serial


def on_connect(client, userdata, flags, rc):
    # 연결이 성공적으로 된다면 완료 메세지 출력
    if rc == 0:
        print("서버와 연결 되었습니다.")
    else:
        print("Bad connection Returned code=", rc)

# 연결이 끊기면 출력
def on_disconnect(client, userdata, flags, rc=0):
    print("연결이 종료 되었습니다.")


def on_publish(client, userdata, mid):
    #print("In on_pub callback mid= ", mid)
    print(f'[{mid}] {userdata}')


# 새로운 클라이언트 생성
client = mqtt.Client()
# 콜백 함수 설정 on_connect(브로커에 접속), on_disconnect(브로커에 접속중료), on_publish(메세지 발행)
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_publish = on_publish
# 로컬 아닌, 원격 mqtt broker에 연결
# address : broker.hivemq.com
# port: 1883 에 연결
client.connect('broker.hivemq.com', 1883)

# 아두이노 연결
py_serial = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
)

while True :
    client.loop_start()

    if py_serial.readable() :
        response = py_serial.readline()
        temp,humi = response[:len(response)-1].decode().split(',')
        text = temp + " " + humi

        #print(text)
        #'test/hello' 라는 topic 으로 메세지 발행
        client.publish('test/send_data', str(text), 1)

    client.loop_stop()
    #time.sleep(2)
# 연결 종료
client.disconnect()