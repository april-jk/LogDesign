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
#完成全日志提取，并能全部保存到pkl文件

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
                content_list = []
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

                    content_dict['EventID'] = domtree.getElementsByTagName('EventID')[0].childNodes[0].data
                    content_dict['Level'] = domtree.getElementsByTagName('Level')[0].childNodes[0].data
                    content_dict['UserID'] = domtree.getElementsByTagName('Security')[0].getAttribute('UserID')
                    content_dict['ProcessID'] = domtree.getElementsByTagName('Execution')[0].getAttribute('ProcessID')
                    content_dict['Computer'] = domtree.getElementsByTagName('Computer')[0].childNodes[0].data
                    # content_dict['IpAddress'] = domtree.getElementsByTagName('IpAddress_EventData')[0].childNodes[0].data

                    # 获取事件详情信息（EventData）
                    for data in domtree.getElementsByTagName('Data'):
                        if len(data.childNodes):
                            content_dict[data.getAttribute('Name') + '_EventData'] = data.childNodes[0].data
                            # print(content_dict)
                        # try:
                        #     content_dict['IpAddress'] = content_dict['IpAddress_EventData']
                        # except:
                        #     content_dict['IpAddress'] = "-"

                    # 获取用户数据信息（UserData）
                    # EventData 与 UserData 一样都是3级子列表，都可以使用以下循环获取完整的日志信息。System 也可以，但需修改为2级
                    for eleone in domtree.getElementsByTagName('UserData'):
                        for eletwo in eleone.childNodes:
                            for elethree in eletwo.childNodes:
                                if elethree.childNodes != () and len(elethree.childNodes) == 1:  # 也可能存在4级，直接忽略
                                    content_dict[elethree.tagName + '_UserData'] = elethree.childNodes[0].data
                        # 归档日志信息
                    content_list.append(content_dict)
                    # 现在evtx节点的信息获取已经完成
                    print(content_list)
        df = DataFrame(content_list).fillna('')  # 让 Nan 为空字符串
        df = DataFrame(content_list).fillna('').sort_values(by=['SystemTime'])   # 按时间排序
        f = open('../pklFile/test_ini.pkl', 'wb')
        pickle.dump(df, f)
        f.close()
        return df
    # 出现一些编码无法识别的日志文件，如果该日志不属于 ['Security', 'System', 'Setup']，则进行忽略
    except (Evtx.BinaryParser.OverrunBufferException, KeyError):
        if os.path.splitext(os.path.basename(evtxpath))[0] not in ['Security', 'System', 'Setup']:
            return DataFrame()
        else:
            raise


print(Log_Get('./Winlog/server.evtx'))
