import datetime
import json
import string
from flask import Flask, redirect, url_for, request,make_response
import logging

datetime=datetime.datetime.now()
app = Flask(__name__)
logging.basicConfig(filename='logger-ana.log', level=logging.INFO)


@app.route('/')
def web_index():
    return '<h1>this log-ana Platform！</h1>'

@app.route('/v1/api/logAudit/winlog', methods=['GET'])
def web_winlog():
    if request.method=='GET':
        # page=int(request.args.get('page'))
        # count=int(request.args.get('count'))
        # data=fetchWinLog_api(page,count)
        # print(date)
        headers={
            'Access-Control-Allow-Headers': 'Access-Control-Allow-Origin,Content-Type',
            'Access-Control-Allow-Origin': '*',
        }
    else:
        return
    return make_response("123",headers)
# @app.route('')






if __name__ == '__main__':
    # data = fetchWinLog_api(1, 100)
    # print(data)
    app.run(host='0.0.0.0', port=8200,debug='true')
