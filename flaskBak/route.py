import datetime
import json
import string
from flask import Flask, redirect, url_for, request
from flaskBak.api.dashboard import getHostNumber_api,getWarnNumber_api,getWeakNumber_api,getLogNumber_api
from flaskBak.api.fetchLog import fetchWinLog_api
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
@app.route('/v1/api/logAudit/winlog', methods=['POST', 'GET'])
def web_winlog():
    date=fetchWinLog_api()
    # print(date)
    return date


# @app.route('/success')
# def success():
#     return 'update ipv6 successfully！'

# @app.route('/test')
# def test():
#     return redirect(url_for('/success'))


# @app.route('/localInfo', methods=['POST', 'GET'])
# def saveIPConfig():
#     if request.method == 'POST':
#         ipv6 = request.form.get('ipv6')
#         ipconfig=request.form.get('ipconfig')
#         lastTime = datetime.strftime("%Y-%m-%d %H:%M:%S")
#         # print(lastTime + "++|++" + ipv6)
#         # print(lastTime+"++|++"+ipv6 + "++|++" + ipconfig + "++|++"+'\n')
#         ipConfigFile = open('ipConfigFile.txt', 'a+')
#         ipConfigFile.write(lastTime + ipconfig +'\n')
#         ipv6File=open('ipv6.txt','a+')
#         ipv6File.write(lastTime+'   >'+ipv6+'<'+'\n')
#         return 'submit success!'
#     else:
#         return 'please submit date through post!'

@app.route('/v1/api/count/lognum', methods=['POST', 'GET'])
def getlognum():
    print(getLogNumber_api())
    num=getLogNumber_api()
    return num
@app.route('/v1/api/count/warnnum', methods=['POST', 'GET'])
def getwarnum():
    return getWarnNumber_api()
@app.route('/v1/api/count/weaknum', methods=['POST', 'GET'])
def getweaknum():
    return getWeakNumber_api()
@app.route('/v1/api/count/hostnum', methods=['POST', 'GET'])
def gethostnum():
    return getHostNumber_api()





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8088,debug='true')
