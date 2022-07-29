import contextlib
import sys
from miscFunc.progress_bar import progress_bar
from datetime import datetime

import pymysql

from config.dbConfig import dbConfig_log

import mmap
import contextlib
import datetime
import os
import pickle
# 这个文件是提取evtx到pkl缓存
import Evtx.BinaryParser
from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view
from xml.dom import minidom
from pandas import DataFrame

from core.time import generateTime




# sql = "SELECT * FROM test "
# # sql = "INSERT INTO test_mysql (name, num, text) VALUES ('{0}','{1}', '{2}')".format('Zarten_1', 1, 'mysql test')
# try:
#     with mysql_conn.cursor() as cursor:
#         cursor.execute(sql)
#         select_result = cursor.fetchone()
#         print(select_result)
# except Exception as e:
#     print(e)

# 这个文件是提取evtx到pkl缓存

'''
evtx to SQL
'''
# # insert
# sql = "INSERT INTO test_mysql (name, num, text) VALUES ('{0}','{1}', '{2}')".format('Zarten_1', 1, 'mysql test')
# try:
#     with mysql_conn.cursor() as cursor:
#         cursor.execute(sql)
#     mysql_conn.commit()
# except Exception as e:
#     mysql_conn.rollback()




#可以根据日志发生时间提取，比如只关注最近一个月，那么提取最近一个月即可，可以大大加速


def exportEVTX(evtxpath):
    '''
    这个函数会解析evtx文件并将其节点解析存放
    :param evtxpath:evtx文件路径:
    :param month:查X年X月之后的数据
    :return:df
    :outputFile:test_new.pkl
    '''
    print("START!")
    try:
        with open(evtxpath, 'r') as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
                content_list = []
                list4624_4625 = []
                fh = FileHeader(buf, 0)

                # 遍历每条日志信息
                for xml, record in evtx_file_xml_view(fh):
                    content_dict = {}
                    domtree = minidom.parseString(xml)

                    # 获取事件标准信息（System）
                    content_dict['Channel'] = domtree.getElementsByTagName('Channel')[0].childNodes[0].data
                    # print(content_dict)['Channel']
                    content_dict['SystemTime'] = str(datetime.datetime.strptime(
                        domtree.getElementsByTagName('TimeCreated')[0].getAttribute('SystemTime')[:19],
                        '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=8))
                    # if not generateTime.formerIsLater(content_dict['SystemTime'], laterTime, ignoreTime):
                    #     print('2')
                    #     continue
                    content_dict['EventID'] = domtree.getElementsByTagName('EventID')[0].childNodes[0].data
                    content_dict['Level'] = domtree.getElementsByTagName('Level')[0].childNodes[0].data
                    content_dict['UserID'] = domtree.getElementsByTagName('Security')[0].getAttribute('UserID')
                    content_dict['ProcessID'] = domtree.getElementsByTagName('Execution')[0].getAttribute('ProcessID')
                    content_dict['Computer'] = domtree.getElementsByTagName('Computer')[0].childNodes[0].data

                    # 获取事件详情信息（EventData）
                    for data in domtree.getElementsByTagName('Data'):
                        if len(data.childNodes):
                            content_dict[data.getAttribute('Name') + '_EventData'] = data.childNodes[0].data

                    # 获取用户数据信息（UserData）
                    # EventData 与 UserData 一样都是3级子列表，都可以使用以下循环获取完整的日志信息。System 也可以，但需修改为2级
                    for eleone in domtree.getElementsByTagName('UserData'):
                        for eletwo in eleone.childNodes:
                            for elethree in eletwo.childNodes:
                                if elethree.childNodes != () and len(elethree.childNodes) == 1:  # 也可能存在4级，直接忽略
                                    content_dict[elethree.tagName + '_UserData'] = elethree.childNodes[0].data
                        # 归档日志信息
                    content_list.append(content_dict)

                    print('1')
                    # 现在evtx节点的信息获取已经完成
        all_log = DataFrame(content_list).fillna('')  # 让 Nan 为空字符串
        all_log = DataFrame(content_list).fillna('').sort_values(by=['SystemTime'])  # 按时间排序
        # f = open('pklFile/test_all_2008.pkl', 'wb')
        f = open(temPKL, 'wb')
        pickle.dump(all_log, f)
        f.close()
        print("export ok!")
        return all_log
    # 出现一些编码无法识别的日志文件，如果该日志不属于 ['Security', 'System', 'Setup']，则进行忽略
    except (Evtx.BinaryParser.OverrunBufferException, KeyError):
        if os.path.splitext(os.path.basename(evtxpath))[0] not in ['Security', 'System', 'Setup']:
            return DataFrame()
        else:
            raise


temPKL='145clj.pkl'
# # exportEVTX('./Winlog/server2012/server.evtx')
# exportEVTX('../Winlog/server2008/1.evtx','2021-09-14 12:12:12',False)
#
# table_name='test'
# sql = "INSERT INTO test_mysql (name, num, text) VALUES ('{0}','{1}', '{2}')".format('Zarten_1', 1, 'mysql test')

# try:
#     with mysql_conn.cursor() as cursor:
#         cursor.execute(sql)
#     mysql_conn.commit()
# except Exception as e:
#     mysql_conn.rollback()

def toSql(PKLFile):
    mysql_conn = pymysql.connect(host=dbConfig_log.get("host"),
                                 port=dbConfig_log.get("port"),
                                 user=dbConfig_log.get("user"),
                                 password=dbConfig_log.get("password"),
                                 db=dbConfig_log.get("db"))
    f = open(PKLFile, 'rb')
    df=pickle.load(f)
    line_all=df.shape[0]
    line_now=0
    for data in df.values:
        line_now+=1
        progress_bar(line_now/line_all)

        index={'channel': '', 'systmtime': '', 'eventid': '', 'level': '', 'targetuserName': '', 'targetdomainname': '',
         'targetsid': '',
         'subjectusersid': '', 'subjectusername': '', 'subjectdominename': '', 'subjectlogonid': '',
         'callprocessname': '',
         'targetusersid': '', 'status': '', 'substatus': '', 'logontype': '', 'logonprocessname': '',
         'workstationname': '', 'processname': '', 'ipaddress': ''}
        dfColon=df.columns
        index['channel']=dfColon.get_loc('Channel')
        index['systemtime']=dfColon.get_loc('SystemTime')
        index['eventid']=dfColon.get_loc('EventID')
        index['level']=dfColon.get_loc('Level')
        index['targetuserName'] = dfColon.get_loc('TargetUserName_EventData')

        index['targetdomainname'] = dfColon.get_loc('TargetDomainName_EventData')
        index['targetsid'] = dfColon.get_loc('TargetSid_EventData')
        index['subjectusersid'] = dfColon.get_loc('SubjectUserSid_EventData')
        index['subjectusername'] = dfColon.get_loc('SubjectUserName_EventData')
        index['subjectdominename'] = dfColon.get_loc('SubjectDomainName_EventData')

        index['subjectlogonid'] = dfColon.get_loc('SubjectLogonId_EventData')
        # index['callprocessname'] = dfColon.get_loc('CallerProcessName_EventData')
        index['targetusersid'] = dfColon.get_loc('TargetUserSid_EventData')
        index['status'] = dfColon.get_loc('Status_EventData')
        index['substatus'] = dfColon.get_loc('SubStatus_EventData')
        index['logontype'] = dfColon.get_loc('LogonType_EventData')

        index['logonprocessname'] = dfColon.get_loc('LogonProcessName_EventData')
        index['workstationname'] = dfColon.get_loc('WorkstationName_EventData')
        index['processname'] = dfColon.get_loc('ProcessName_EventData')
        index['ipaddress'] = dfColon.get_loc('IpAddress_EventData')


        sql = "INSERT INTO `testlog`" \
              " (`channel`, `systemtime`, `eventid`, `level`, `targetuserName`, " \
              "`targetdomainname`, `targetsid`, `subjectusersid`, `subjectusername`, `subjectdominename`," \
              " `subjectlogonid`, `targetusersid`, `status`, `substatus`, `logontype`, " \
              "`logonprocessname`, `workstationname`, `processname`, `ipaddress`) VALUES " \
              "('{}', '{}', '{}', '{}', '{}', " \
              "'{}', '{}', '{}', '{}', '{}'," \
              " '{}', '{}', '{}', '{}','{}'," \
              " '{}', '{}', '{}', '{}')".format(
            data[index['channel']], data[index['systemtime']], data[index['eventid']], data[index['level']],data[index['targetuserName']],
            data[index['targetdomainname']],data[index['targetsid']],data[index['subjectusersid']],data[index['subjectusername']],data[index['subjectdominename']],
            data[index['subjectlogonid']],data[index['targetusersid']],data[index['status']],data[index['substatus']],data[index['logontype']],
            data[index['logonprocessname']],data[index['workstationname']],data[index['processname']],data[index['ipaddress']])
        try:
            with mysql_conn.cursor() as cursor:
                cursor.execute(sql)
            mysql_conn.commit()
            # print('commit!')
        except Exception as e:
            mysql_conn.rollback()
            print(e)
    print("\n[+]allToSQL!")

# toSql(temPKL)
exportEVTX(temPKL)