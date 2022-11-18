import json

from _cffi_backend import typeof

from flaskBak.sql.fetchLog import fetchWinLog
# def fetchWinLog(hostName,dateTime1,datetime2,page,ip,domain):
#     data_fetched=''
#     return data_fetched

def fetchWinLog_api(page,count,host,eventid):
    logData=json.dumps(fetchWinLog(page,count,host,eventid))
    # print(logData)
    return logData
# data=fetchWinLog_api()
# print(data)
# print(typeof(date))
# print(1)
if __name__ == '__main__':
    a=fetchWinLog_api()
    print(a)