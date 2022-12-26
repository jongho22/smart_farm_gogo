import paho.mqtt.client as mqtt
import pymongo

from flask import *
from pymongo import MongoClient
from datetime import datetime, timedelta

import json
import time


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
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        send_end_date = str(end_date).split(" ")[0]
        send_start_date = str(start_date).split(" ")[0]
        end_date = end_date+timedelta(days=1)

        results = db_col.find({"rev_date": {"$gte": start_date, "$lte": end_date}}).sort("_id",-1)

        return render_template('graph.html',data=results,start_date = send_start_date ,end_date = send_end_date)
    if request.method == 'GET':
        return render_template('graph.html')

# 실시간 그래프를 위한 json생성기
@app.route('/graph')
def chart_data() :
    def generate_raw_data() :
        while True :
            raw_data = db_col.find().sort("_id",-1).limit(1)[0]
            #print(f'날짜+시간: {raw_data["rev_date"]} 온도 : {raw_data["temp"]}  습도 : {raw_data["humi"]}')
            
            json_data = json.dumps({'time':str(raw_data["rev_date"]).split(" ")[1],'value1':raw_data["temp"],'value2':raw_data["humi"]})
            yield f"data: {json_data}\n\n"
            time.sleep(61)

    return Response(generate_raw_data(), mimetype='text/event-stream')

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
    app.run(host= "0.0.0.0", debug=True, port=9999, threaded = True)



