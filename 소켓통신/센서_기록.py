import serial
import time
from datetime import datetime

def sensor_log(t_input,n_hour) : 

    py_serial = serial.Serial(
        port='COM8',   # Window
        baudrate=9600, # 보드 레이트 (통신 속도)
    )
    now = datetime.now()
    temp_humi_string = ""
    start = time.time()  # 시작 시간 저장
    check_time_start = time.time()
    start_time =f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}"

    while True:
    
        if py_serial.readable() : # 아두이노에서 '온도', '습도'를 읽어 올수 있고 t_input 초가 지났을 때만 값을 저장
            now = datetime.now()
            response = py_serial.readline()
            temp, humi = response[:len(response)-1].decode().split(',') # 디코딩 후, 출력 (가장 끝의 \n을 없애주기위해 슬라이싱 사용)
            t = f"{str(now.hour)}:{str(now.minute)}:{str(now.second)}"  # 온도,습도 측정 했을 때의 시간
            save_string = str(t) +", "+ temp + ", " + humi              # 출력값 결합
            
            if time.time() - check_time_start >= t_input :
                temp_humi_string = temp_humi_string + save_string
                check_time_start = time.time()
                print(save_string) # 출력값 확인

        if time.time() - start >= n_hour : #* 3600:  #1시간 = 3600초
            end_time = f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}"
            f = open(f'{start_time}_{end_time}.txt', 'a', encoding='utf-8')
            f.write(temp_humi_string)
            f.close()
            temp_humi_string = ""  # 초기화
            start = time.time()
            start_time =f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}"

        
sensor_log(10,30) # 첫번째=> 시간 간격(초), 두번째=> 파일 저장 간격(시)
        