from _cffi_backend import typeof

from flaskBak.sql.fetchLog import fetchWinLog
# def fetchWinLog(hostName,dateTime1,datetime2,page,ip,domain):
#     data_fetched=''
#     return data_fetched

def fetchWinLogAPI():
    logDate=fetchWinLog()
    return logDate
date=fetchWinLogAPI()
print(date)
# print(typeof(date))
# print(1)