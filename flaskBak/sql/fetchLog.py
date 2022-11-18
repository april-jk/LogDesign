import collections
import json
from datetime import date, datetime
from time import sleep

import pandas as pd
import pymysql
from _cffi_backend import typeof, string

from  config.dbConfig import dbConfig_log

mysql_conn = pymysql.connect(host=dbConfig_log.get("host"),
                             port=dbConfig_log.get("port"),
                             user=dbConfig_log.get("user"),
                             password=dbConfig_log.get("password"),
                             db=dbConfig_log.get("db"))
# systemtime          SystemTime
# eventid             EventID
# currUser            subjectusername
# targetUser          TargetUserName
# domain              subjectdominename
# targetDomain        TargetDomainName
# ipaddr              ipaddress

def fetchWinLog(page,count,host,eventid):
    if eventid==0:
        sql = "SELECT SystemTime,EventID,subjectusername,TargetUserName,subjectdominename,TargetDomainName,ipaddress" \
              " FROM `" + host + "` limit " + str((page - 1) * count) + "," + str(page * count)
    else:
        eventid=str(eventid)
        sql = "SELECT SystemTime,EventID,subjectusername,TargetUserName,subjectdominename,TargetDomainName,ipaddress" \
              " FROM `" + host +"` where eventid ="+ eventid + " limit " + str((page - 1) * count) + "," + str(page * count)
    # sql = "INSERT INTO test_mysql (name, num, text) VALUES ('{0}','{1}', '{2}')".format('Zarten_1', 1, 'mysql test')
    data = []
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            # mysql_conn.close()
            # data = []

            # systemtime          SystemTime
            # eventid             EventID
            # currUser            subjectusername
            # targetUser          TargetUserName
            # domain              subjectdominename
            # targetDomain        TargetDomainName
            # ipaddr              ipaddress

            for row_ in rows:
                # global data
                d=collections.OrderedDict()
                d['systemtime']=row_[0].strftime('%Y-%m-%d %H:%M:%S')
                d['eventid']=row_[1]
                d['currUser']=row_[2]
                d['targetUser']=row_[3]
                d['domain']=row_[4]
                d['targetDomain']=row_[5]
                d['ipaddr']=row_[6]
                data.append(d)
            # json_str=json.dumps(data)
            # print(json_str)
    except Exception as e:
        print(e)
        print("sql:"+sql)
    return data
# fetchWinLog()
if __name__ == '__main__':
    a=fetchWinLog(1,100)
    print(a)
    # sleep(10)
    # a=fetchWinLog()
    # print(a)

