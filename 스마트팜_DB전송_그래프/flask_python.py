from flask import *
from pymongo import MongoClient
from datetime import datetime

import json
import time

app = Flask(__name__)

my_client = MongoClient("mongodb://localhost:27017/")

db = my_client['test_db']
db_col = db.test_data

@app.route('/')
def graph() :
    return render_template('graph.html')

@app.route('/graph')
def chart_data() :
    def generate_raw_data() :
        while True :
            raw_data = db_col.find().sort("_id",-1).limit(1)[0]
            print(f'시간 : {raw_data["rev_time"]}  온도 : {raw_data["temp"]}  습도 : {raw_data["humi"]}')
            

            json_data = json.dumps({'time':raw_data["rev_time"],'value1':raw_data["temp"],'value2':raw_data["humi"]})
            yield f"data: {json_data}\n\n"
            time.sleep(1)

    return Response(generate_raw_data(), mimetype='text/event-stream')

if __name__ == '__main__' :
    app.run(debug=True, port=9999, threaded = True)



