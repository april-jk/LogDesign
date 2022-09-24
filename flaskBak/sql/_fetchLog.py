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


            rowarray_list=[]
            # for row in rows:
            #     t=(row[0],row[1],row[2],row[3],row[4],row[5],row[6])
            #     rowarray_list.append(t)
            # j=json.dumps(rowarray_list,cls='ComplexEncoder',)
            # with open("rowarray.js","w") as f:
            #     f.write(j)
            object_list=[]
            json_str='{'
            for row_ in rows:
                d=collections.OrderedDict()
                d['SystemTime']=row_[0].strftime('%Y-%m-%d %H:%M:%S')
                d['EventID']=row_[1]
                d['subjectusername']=row_[2]
                d['TargetUserName']=row_[3]
                d['subjectdominename']=row_[4]
                d['TargetDomainName']=row_[5]
                d['ipaddress']=row_[6]
                json_str=json_str+','+'\"systemtime\":\"'+row_[0]+'\",'+'\"eventid\":\"'+row_[1]+\
                         '\",\"currUser\":\"'+row_[2]+'\",\"targetUser\":\"'+row_[3]+'\",\"domain\":'+row_[4]+\
                         '\",\"targetDomain\":\"'+row_[5]+'\",\"ipaddr\":\"'+row_[6]+'\"}'
                # print(json_str)
                # object_list.append(d)
                # dict(zip(d.keys(),d.values()))
            # j=json.dumps(object_list,cls='ComplexEncoder',skipkeys='true',ensure_ascii='False')
            print(json_str)
            # with open('test.js',"w") as f:
            #     f.write(j)

            # print(select_result)
            # print('\n')
            # print(typeof(select_result))

    except Exception as e:
        print(e)
    return
fetchWinLog()
if __name__ == '__main__':
    fetchWinLog()



class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
