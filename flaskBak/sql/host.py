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


def getHostList():
    mysql_conn = sqllog_con()
    sql = 'select table_name from information_schema.TABLES where TABLE_SCHEMA ="LogAudit_log"'
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute(sql)
            List = cursor.fetchall()
            hostList = []
            for host in List:
                hostList.append(host[0])
            mysql_conn.close()
    except Exception as e:
        print(e)
    return hostList


# def getLogNumber():
#     '''
#     获取日志数量
#     :return: 日志数量
#     '''
#     mysql_conn=sqllog_con()
#     sql='select count(logid) from testlog'
#     try:
#         with mysql_conn.cursor() as cursor:
#             cursor.execute(sql)
#             numLog = cursor.fetchall()
#             mysql_conn.close()
#     except Exception as e:
#         print(e)
#     return numLog[0][0]

def getLogNumber():
    '''
    获取日志数量
    :return: 日志数量
    '''
    mysql_conn=sqllog_con()
    sql='select count(logid) from '
    num=0
    try:
        hostList=getHostList()
        mysql_conn = sqllog_con()
        for tableName in hostList:
            try:
                sql += tableName
                with mysql_conn.cursor() as cursor:
                    cursor.execute(sql)
                    num = cursor.fetchall()
                    num=num[0][0]
                    # print(num)
            except:
                continue
    except Exception as e:
        print(e)
    mysql_conn.close()
    # print("num:"+str(num))
    return num


def getWarnNumber():
    # mysql_conn=sqlAna_con()
    # sql=''
    # try:
    #     with mysql_conn.cursor() as cursor:
    #         cursor.execute(sql)
    #         numLog = cursor.fetchall()
    #         mysql_conn.close()
    # except Exception as e:
    #     print(e)
    # return numLog[0][0]
    return

def getWeakNumber():
    # mysql_conn=sqlAna_con()
    # sql=''
    # try:
    #     with mysql_conn.cursor() as cursor:
    #         cursor.execute(sql)
    #         numLog = cursor.fetchall()
    #         mysql_conn.close()
    # except Exception as e:
    #     print(e)
    # return numLog[0][0]
    return
def getHostNumber():
    num=getHostList()
    num=len(num)
    return num



if __name__ == '__main__':
    # q=getLogNumber()
    # # print(type(q))
    # print(q)
    print(getHostNumber())



