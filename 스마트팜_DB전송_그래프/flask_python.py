from flask import *
from pymongo import MongoClient
from datetime import datetime, timedelta
from time import sleep
from controller import mqtt_controller
from sensor_rev import Sensor
from threading import Thread

import json, math



app = Flask(__name__)

# 몽고 DB 연결
my_client = MongoClient("mongodb://localhost:27017/")

db = my_client['test_db']
db_col = db.test_data

# 메인 페이지
@app.route('/',methods=['POST','GET'])
def graph() :
    limit = 10 # DB 테이블 몇개 보여줄지
    block_size = 10 # 페이지네이션 블럭 개수
    
    if request.method == 'POST':
        page = request.args.get('page', type=int, default=1)  # 페이지
        
        try : # DB 조회 버튼을 눌렀을때
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            
        except : # DB 조회 버튼을 누르지 않았을때
            today = datetime.today()
            start_date = db_col.find_one()['rev_date']
            start_date = str(start_date).split(" ")[0]
            end_date = (today+timedelta(days=1)).strftime("%Y-%m-%d")

        try : # 창문 환기 시스템에 값을 전달 헀을때
            val1 = None
            val2 = str(request.form['length'])

            if request.form['button'] == 'close':
                val1 = 'down'
            elif request.form['button'] == 'open':
                val1 = 'up'

            val = val1 +" "+ val2
            print(val)
            with mqtt_controller(val,'test/actuator') as m:
                m.main()

        except : # 창문 환기 시스템에 값을 전달하지 않았을때
            pass

        try : # 수중 모터(물주기)를 작동시켰을때
            val = int(request.form['water_active'])

            if request.form['button'] == '물 주기':
                with mqtt_controller(val, 'test/send_data') as m:
                    m.main()
                    print("물 주기")

        except : # 수중 모터(물주기)를 작동시키지 않았을때
            pass

    if request.method == 'GET':
        today = datetime.today()
        start_date = db_col.find_one()['rev_date']
        start_date = str(start_date).split(" ")[0]
        end_date = (today+timedelta(days=1)).strftime("%Y-%m-%d")

        start_date = request.args.get('start_date', type=str, default=start_date)
        end_date = request.args.get('end_date', type=str, default=end_date)
        page = request.args.get('page', type=int, default=1)  # 페이지

    # DB 조회를 위한 날짜 처리    
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    send_start_date = str(start_date).split(" ")[0]
    send_end_date = str(end_date).split(" ")[0]

    # 해당 날짜의 데이터를 DB에서 가져오기
    results = db_col.find({"rev_date": {"$gte": start_date, "$lte": end_date}}).sort("_id",-1).skip((page-1)*limit).limit(limit)
    total_data  = db_col.count_documents({})
    
    # 페이지네이션 처리
    last_page_num = math.ceil(total_data / limit) 
    block_num = int((page - 1) / block_size)
    block_start = (block_size * block_num) + 1
    block_end = block_start + (block_size - 1)

    return render_template('index.html',data=results,start_date = send_start_date ,end_date = send_end_date,limit=limit,page=page,block_start=block_start,block_end=block_end,last_page_num=last_page_num,total_data=total_data)

# 실시간 그래프를 위한 json생성기
@app.route('/graph')
def chart_data() :
    def generate_raw_data() :
        while True :
            raw_data = db_col.find().sort("_id",-1).limit(1)[0]
            #print(f'날짜+시간: {raw_data["rev_date"]} 온도 : {raw_data["temp"]}  습도 : {raw_data["humi"]}')

            # 빗물 감지 센서 => 비오는 여부 판단
            if int(raw_data['rain']) < 1000 :
                rain = "빗물 감지"
            else :
                rain = "빗물 미 감지"

            # 조도 센서 => 밤낮 여부 확인
            if int(raw_data["light"]) > 550 :
                light = "밝음"
            else : 
                light = "어두움"

            json_data = json.dumps({'time':str(raw_data["rev_date"]).split(" ")[1],'value1':raw_data["temp"],'value2':raw_data["humi"],'value3':raw_data["light"],'value4' :raw_data['rain'], 'value4_1' : rain,'value3_1': light})
            yield f"data: {json_data}\n\n"
            sleep(61)

    return Response(generate_raw_data(), mimetype='text/event-stream')

''' 전체 DB 조회 그래프 만들다가 실패
@app.route('/graph2')
def chart_data2() :
    def generate_raw_data2() :
        n = db_col.estimated_document_count()
        print(f'DB => {n}')
        #jump = (n/100)*2
        #print(round(jump))
        for i in range(n) :
            raw_data = db_col.find().sort("_id",1)[i]
            #print(f'날짜+시간: {raw_data["rev_date"]} 온도 : {raw_data["temp"]}  습도 : {raw_data["humi"]}')
            
            json_data = json.dumps({'date':str(raw_data["rev_date"]).split(" ")[0],'time':str(raw_data["rev_date"]).split(" ")[1],'value1':raw_data["temp"],'value2':raw_data["humi"],'num':n})
            yield f"data: {json_data}\n\n"
        time.sleep(300)
    
    return Response(generate_raw_data2(), mimetype='text/event-stream')
'''

if __name__ == '__main__' :

    temp = Sensor()
    temp.daemon = False
    temp.start()

    kwargs = {'host': "0.0.0.0", 'port':'9999', 'threaded':True, 'debug':False}
    flaskThread = Thread(target=app.run, daemon=True, kwargs=kwargs).start()
    # app.run(host= "0.0.0.0", debug=True, port=9999, threaded = True)