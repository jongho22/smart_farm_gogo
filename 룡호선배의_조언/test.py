from socket import *

port = 2577

clientSock = socket(AF_INET, SOCK_STREAM)
clientSock.connect(('203.252.240.67', port))

print('접속 완료')

while True:
    recvData = clientSock.recv(1024)
    print('상대방 :', recvData.decode('utf-8'))

    sendData = input('>>>')
    clientSock.send(sendData.encode('utf-8'))