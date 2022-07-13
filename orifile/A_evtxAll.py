import mmap
import contextlib
import datetime
import os
import pickle

import Evtx.BinaryParser
from Evtx.Evtx import FileHeader
from Evtx.Views import evtx_file_xml_view
from xml.dom import minidom
from pandas import DataFrame

def Log_Get(evtxpath):
    '''
    这个函数会解析evtx文件并将其节点解析存放至list嵌套的字典中
    :param evtx文件路径:
    :return:df
    :outputFIle:test_ini.pkl
    '''
    print("START!")
    try:
        with open(evtxpath, 'r') as f:
            with contextlib.closing(mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)) as buf:
                fh = FileHeader(buf, 0)

                # 遍历每条日志信息
                for xml, record in evtx_file_xml_view(fh):
                    content_dict = {}
                    domtree = minidom.parseString(xml)
                    # 获取事件详情信息（EventData）
                    content_dict['EventID'] = domtree.getElementsByTagName('EventID')[0].childNodes[0].data

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
                    if content_dict['EventID'] == '4624' and  content_dict[29] !='-':
                        try:
                            print(content_dict)
                        except:
                            continue

    # 出现一些编码无法识别的日志文件，如果该日志不属于 ['Security', 'System', 'Setup']，则进行忽略
    except (Evtx.BinaryParser.OverrunBufferException, KeyError):
        if os.path.splitext(os.path.basename(evtxpath))[0] not in ['Security', 'System', 'Setup']:
            return DataFrame()
        else:
            raise


#Log_Get('./Winlog/yoga/Security.evtx')
# Log_Get('./Winlog/server2012/RDP_securityLog.evtx')
# Log_Get('./Winlog/server2012/server.evtx')
Log_Get('./Winlog/server2012/exportBeforeClean.evtx')


'''
{'EventID': '1102', 'SubjectUserSid_UserData': 'S-1-5-21-1390822584-1902517743-2670227040-500', 'SubjectUserName_UserData': 'Administrator', 'SubjectDomainName_UserData': '10_0_12_14', 'SubjectLogonId_UserData': '0x0000000001aeb181'}

'''