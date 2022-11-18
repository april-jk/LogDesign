import datetime
import json
import string
from flask import Flask, redirect, url_for, request,make_response
from flaskBak.api.dashboard import getHostNumber_api, getWarnNumber_api, getWeakNumber_api, getLogNumber_api, \
    getNumber_api, getDashList
from flaskBak.api.fetchLog import fetchWinLog_api
from flaskBak.api.host import getHostList_api, getHostList_easy_api
from flaskBak.api.login import loginVerify
import logging

datetime=datetime.datetime.now()
app = Flask(__name__)
logging.basicConfig(filename='logger.log', level=logging.INFO)


@app.route('/')
def web_index():
    return 'index'

# @app.route('/dashboard', methods=['POST', 'GET'])
# def web_toIndex():
#     return 'dashboad'
#
# @app.route('/v1/api/logAudit/logAudit', methods=['POST', 'GET'])
# def web_logAudit():
#     return







@app.route('/v1/api/logAudit/winlog', methods=['GET'])
def web_winlog():
    if request.method=='GET':
        page=int(request.args.get('page'))
        count=int(request.args.get('count'))
        host=str(request.args.get('host'))
        eventid=int(request.args.get('eventid'))
        print(eventid)
        #这存在sql注入
        data=fetchWinLog_api(page,count,host,eventid)
        # print(date)
        headers={
            'Access-Control-Allow-Headers': 'Access-Control-Allow-Origin,Content-Type',
            'Access-Control-Allow-Origin': '*',
        }
    else:
        return
    return make_response(data,headers)



# @app.route('/success')
# def success():
#     return 'update ipv6 successfully！'

# @app.route('/test')
# def test():
#     return redirect(url_for('/success'))



@app.route('/v1/api/count/dashboard', methods=['POST', 'GET'])
def getlognum():
    # print(getLogNumber_api())
    dashnum=getNumber_api()
    headers = {
        'Access-Control-Allow-Headers': 'Access-Control-Allow-Origin,Content-Type',
        'Access-Control-Allow-Origin': '*',
    }
    return make_response(dashnum, headers)


@app.route('/v1/api/host/dashList',methods=['POST','GET'])
def getdashList():
    data=getDashList()
    headers={
            'Access-Control-Allow-Headers': 'Access-Control-Allow-Origin,Content-Type',
            'Access-Control-Allow-Origin': '*',
        }
    return make_response(data,headers)


@app.route('/v1/api/host/hostList',methods=['POST','GET'])
def getHost():
    data = getHostList_api()
    headers = {
        'Access-Control-Allow-Headers': 'Access-Control-Allow-Origin,Content-Type',
        'Access-Control-Allow-Origin': '*',
    }
    return make_response(data, headers)
@app.route('/v1/api/host/hostList_easy',methods=['POST','GET'])
def getHost_easy():
    data=getHostList_easy_api()
    headers = {
        'Access-Control-Allow-Headers': 'Access-Control-Allow-Origin,Content-Type',
        'Access-Control-Allow-Origin': '*',
    }
    return make_response(data, headers)



@app.route('/v1/api/login',methods=['POST'])
def login():
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        headers = {
            'Access-Control-Allow-Headers': 'Access-Control-Allow-Origin,Content-Type',
            'Access-Control-Allow-Origin': '*',
        }
        data = loginVerify(username,password)
        return make_response(data, headers)





if __name__ == '__main__':
    # data = fetchWinLog_api(1, 100)
    # print(data)
    app.run(host='0.0.0.0', port=8111,debug='true')


# /home/ubuntu/LogDesign
# runfile('/home/ubuntu/LogDesign/flaskBak/route.py', wdir='/home/ubuntu/LogDesign/flaskBak')