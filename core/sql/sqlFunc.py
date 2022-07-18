import pymysql
from core.sql.dbConfig import dbConfig

mysql_conn = pymysql.connect(host= dbConfig.get("host"),
                             port= dbConfig.get("port"),
                             user= dbConfig.get("user"),
                             password= dbConfig.get("password"),
                             db= dbConfig.get("db"))

