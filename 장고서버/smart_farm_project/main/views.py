from django.shortcuts import render
from django.http import HttpResponse

# 몽고 DB
from pymongo import MongoClient
my_client = MongoClient("mongodb://localhost:27017/")
db = my_client['test_db']
db_col = db.test_data
import json, time
from datetime import datetime, timedelta

# Create your views here.
def chart_data(request) :
    def generate_raw_data() :
        while True :
            raw_data = db_col.find().sort("_id",-1).limit(1)[0]
            print(f'날짜 : {raw_data["rev_date"]} 시간 : {raw_data["rev_time"]}  온도 : {raw_data["temp"]}  습도 : {raw_data["humi"]}')
            
            json_data = json.dumps({'time':raw_data["rev_time"],'value1':raw_data["temp"],'value2':raw_data["humi"]})
            f"data: {json_data}\n\n"
            time.sleep(1)

    return HttpResponse(generate_raw_data(), content_type='text/event-stream')
    
def date_range(start, end):
    try :
        start = datetime.strptime(start, "%Y-%m-%d")
        end = datetime.strptime(end, "%Y-%m-%d")
        dates = [(start + timedelta(days=i)).strftime("%Y-%m-%d") for i in range((end-start).days+1)]
    except :
        dates = []
    return dates

def index(request) :
    
    return render(request,'graph.html')