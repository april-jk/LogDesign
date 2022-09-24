'''
日志数量、告警数量、脆弱性数量、资产数量
'''
import pymysql
from  config.dbConfig import dbConfig_log
from  config.dbConfig import dbConfig_Ana
from  config.dbConfig import dbConfig_admin

def sqllog_con():
    mysql_conn = pymysql.connect(host=dbConfig_log.get("host"),
                                 port=dbConfig_log.get("port"),
                                 user=dbConfig_log.get("user"),
                                 password=dbConfig_log.get("password"),
                                 db=dbConfig_log.get("db"))
    return mysql_conn
def sqlAna_con():
    mysql_conn = pymysql.connect(host=dbConfig_Ana.get("host"),
                                 port=dbConfig_Ana.get("port"),
                                 user=dbConfig_Ana.get("user"),
                                 password=dbConfig_Ana.get("password"),
                                 db=dbConfig_Ana.get("db"))
    return mysql_conn
def sqladmin_con():
    mysql_conn = pymysql.connect(host=dbConfig_admin.get("host"),
                                 port=dbConfig_admin.get("port"),
                                 user=dbConfig_admin.get("user"),
                                 password=dbConfig_admin.get("password"),
                                 db=dbConfig_admin.get("db"))
    return mysql_conn


def getLogNumber():
    '''
    获取日志数量
    :return: 日志数量
    '''
    mysql_conn=sqllog_con()
    sql='select count(logid) from testlog'
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            numLog = cursor.fetchall()
            mysql_conn.close()
    except Exception as e:
        print(e)
    return numLog[0][0]

def getWarnNumber():
    mysql_conn=sqlAna_con()
    sql=''
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            numLog = cursor.fetchall()
            mysql_conn.close()
    except Exception as e:
        print(e)
    return numLog[0][0]

def getWeakNumber():
    mysql_conn=sqlAna_con()
    sql=''
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            numLog = cursor.fetchall()
            mysql_conn.close()
    except Exception as e:
        print(e)
    return numLog[0][0]
def getHostNumber():
    mysql_conn=sqlAna_con()
    sql=''
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            numLog = cursor.fetchall()
            mysql_conn.close()
    except Exception as e:
        print(e)
    return numLog[0][0]



if __name__ == '__main__':
    q=getLogNumber()
    print(type(q))
    print(q)



