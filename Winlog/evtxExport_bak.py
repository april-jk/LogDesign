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
today=datetime.datetime.today()

#可以根据日志发生时间提取，比如只关注最近一个月，那么提取最近一个月即可，可以大大加速

def exportEVTX(evtxpath):
    '''
    这个函数会解析evtx文件并将其节点解析存放
    :param evtx文件路径:
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
        f = open('pklFile/test_all_2008.pkl', 'wb')
        pickle.dump(all_log, f)
        f.close()
        return all_log
    # 出现一些编码无法识别的日志文件，如果该日志不属于 ['Security', 'System', 'Setup']，则进行忽略
    except (Evtx.BinaryParser.OverrunBufferException, KeyError):
        if os.path.splitext(os.path.basename(evtxpath))[0] not in ['Security', 'System', 'Setup']:
            return DataFrame()
        else:
            raise


# exportEVTX('./Winlog/server2012/server.evtx')
exportEVTX('./Winlog/server2008/1.evtx')
