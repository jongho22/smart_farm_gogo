import serial
import time
import socket

#print("테스트")
client = socket.socket()
client.connect(('203.252.240.64',22))
py_serial = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
)

while True :
    if py_serial.readable() :
        response = py_serial.readline()
        temp,humi = response[:len(response)-1].decode().split(',')
        text = temp + " " + humi
        time.sleep(1)
        client.send(bytes(text,'utf-8'))
        print(repr(client.recv(1024).decode()))