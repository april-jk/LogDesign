import pymysql
from config.dbConfig import dbConfig_admin

mysql_conn = pymysql.connect(host= dbConfig_admin.get("host"),
                             port= dbConfig_admin.get("port"),
                             user= dbConfig_admin.get("user"),
                             password= dbConfig_admin.get("password"),
                             db= dbConfig_admin.get("db"))

#   pymysql   https://zhuanlan.zhihu.com/p/51553625

#insert
# sql = "INSERT INTO test_mysql (name, num, text) VALUES ('{0}','{1}', '{2}')".format('Zarten_1', 1, 'mysql test')
# try:
#     with mysql_conn.cursor() as cursor:
#         cursor.execute(sql)
#     mysql_conn.commit()
# except Exception as e:
#     mysql_conn.rollback()

#modify
# sql = "UPDATE test_mysql SET name = '{0}' WHERE text = '{1}'".format('Zarten_2', 'mysql test')
# try:
#     with mysql_conn.cursor() as cursor:
#         cursor.execute(sql)
#     mysql_conn.commit()
# except Exception as e:
#     print(e)
#     mysql_conn.rollback()


#测试
sql = "SELECT * FROM test_mysql WHERE num = '{0}'".format(1)
try:
    with mysql_conn.cursor() as cursor:
        cursor.execute(sql)
        select_result = cursor.fetchone()
        print(select_result)
except Exception as e:
    print(e)


def test():
    return



if __name__ == '__main__':
    test()
