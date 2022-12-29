import paho.mqtt.client as mqtt
import pymongo

from flask import *
from pymongo import MongoClient
from datetime import datetime, timedelta

import json

from time import time
from time import sleep

from actuator_send import mqtt_actuator
from sensor_rev import Sensor

from threading import Thread

#센서 mqtt

app = Flask(__name__)

my_client = MongoClient("mongodb://localhost:27017/")

db = my_client['test_db']
db_col = db.test_data

def date_range(start, end):
    try :
        start = datetime.strptime(start, "%Y-%m-%d")
        end = datetime.strptime(end, "%Y-%m-%d")
        dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
    except :
        dates = []
    return dates

# 메인 페이지
@app.route('/',methods=['POST','GET'])
def graph() :
    if request.method == 'POST':
        # if request.form['inquiry'] == "조회":
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        send_end_date = str(end_date).split(" ")[0]
        send_start_date = str(start_date).split(" ")[0]
        end_date = end_date+timedelta(days=1)

        results = db_col.find({"rev_date": {"$gte": start_date, "$lte": end_date}}).sort("_id",-1)
        return render_template('index.html',data=results,start_date = send_start_date ,end_date = send_end_date)

    if request.method == 'GET':
        return render_template('index.html')

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

@app.route('/actuator', methods = ['POST', 'GET'])
def actuator():
    if request.method == 'POST':
        val1 = None
        val2 = float(request.form['length'])
        if request.form['button'] == 'close':
            val1 = 'down'
        elif request.form['button'] == 'open':
            val1 = 'up'
        mq_ac = mqtt_actuator(val1, val2)
        mq_ac.main()
    return render_template('index.html')

    '''
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