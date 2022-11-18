import pymysql
from config.dbConfig import dbConfig_log, dbConfig_Ana, dbConfig_admin


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

'''
数据库表的创建和删除用 存储过程  
'''



def createTableOnLog():
    sqllog_con()