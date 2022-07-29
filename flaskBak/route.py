import datetime
import string
from flask import Flask, redirect, url_for, request
from flaskBak.api import fetchLog
import logging

datetime=datetime.datetime.now()
app = Flask(__name__)
logging.basicConfig(filename='logger.log', level=logging.INFO)


@app.route('/')
def web_index():
    return 'index'

@app.route('/dashboard', methods=['POST', 'GET'])
def web_toIndex():
    return 'dashboad'

@app.route('/logAudit', methods=['POST', 'GET'])
def web_logAudit():
    return
@app.route('/logAudit/winlog', methods=['POST', 'GET'])
def web_winlog():
    date=fetchLog()
    return date


@app.route('/success')
def success():
    return 'update ipv6 successfully！'

# @app.route('/test')
# def test():
#     return redirect(url_for('/success'))


@app.route('/localInfo', methods=['POST', 'GET'])
def saveIPConfig():
    if request.method == 'POST':
        ipv6 = request.form.get('ipv6')
        ipconfig=request.form.get('ipconfig')
        lastTime = datetime.strftime("%Y-%m-%d %H:%M:%S")
        # print(lastTime + "++|++" + ipv6)
        # print(lastTime+"++|++"+ipv6 + "++|++" + ipconfig + "++|++"+'\n')
        ipConfigFile = open('ipConfigFile.txt', 'a+')
        ipConfigFile.write(lastTime + ipconfig +'\n')
        ipv6File=open('ipv6.txt','a+')
        ipv6File.write(lastTime+'   >'+ipv6+'<'+'\n')
        return 'submit success!'
    else:
        return 'please submit date through post!'






if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8089,debug='true')
