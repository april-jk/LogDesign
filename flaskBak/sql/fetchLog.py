import collections
import json
from datetime import date, datetime
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

def fetchWinLog():
    sql = "SELECT SystemTime,EventID,subjectusername,TargetUserName,subjectdominename,TargetDomainName,ipaddress" \
          " FROM testlog limit 0,100"
    # sql = "INSERT INTO test_mysql (name, num, text) VALUES ('{0}','{1}', '{2}')".format('Zarten_1', 1, 'mysql test')
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            rows = cursor.fetchall()
            mysql_conn.close()

            data = []
            for row_ in rows:
                d=collections.OrderedDict()
                d['SystemTime']=row_[0].strftime('%Y-%m-%d %H:%M:%S')
                d['EventID']=row_[1]
                d['subjectusername']=row_[2]
                d['TargetUserName']=row_[3]
                d['subjectdominename']=row_[4]
                d['TargetDomainName']=row_[5]
                d['ipaddress']=row_[6]
                data.append(d)
            # json_str=json.dumps(data)
            # print(json_str)

    except Exception as e:
        print(e)
    return data
# fetchWinLog()
if __name__ == '__main__':
    a=fetchWinLog()
    print(a)

