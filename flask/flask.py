import datetime
import string
from flask import Flask, redirect, url_for, request
import logging

datetime=datetime.datetime.now()
app = Flask(__name__)
logging.basicConfig(filename='logger.log', level=logging.INFO)


# 日志部分先一留

@app.route('/success')
def success():
    return 'update ipv6 successfully！'

@app.route('/test')
def test():
    return redirect(url_for('/success'))



@app.route('/')
def index():
    return 'welcome to homepage,compile time: '+ datetime.strftime("%Y-%m-%d %H:%M:%S")


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


@app.route('/getInfo', methods=['GET'])
def getInfo(ipv6, ipconfig):
    type = request.form['type']
    if type == 'ipv6':
        return ipv6
    elif type == 'ipconfig':
        return ipconfig
    elif type == 'all':
        return ipconfig + "|"
    else:
        return '500'



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)
