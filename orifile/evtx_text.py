'''
提取指定事件id的相关信息
'''
# -*- coding:UTF-8 -*-
import re

import Evtx.Evtx as evtx
import Evtx.Views as e_views
from xml.etree import ElementTree

if __name__ == '__main__':
    # Windows事件日志路径
    EvtxPath = r"./SelectedLogs/server.evtx"

    # 解析Windows事件日志
    with evtx.Evtx(EvtxPath) as log:
        for record in log.records():
            xml = record.xml().replace(''' xmlns="http://schemas.microsoft.com/win/2004/08/events/event"''',"")
            Eroot = ElementTree.fromstring(xml)
            # 事件ID
            EventID = Eroot.findall('System')[0].find('EventID').text
            # 计算机名称
            Computer = Eroot.findall('System')[0].find('Computer').text
            # 事件时间
            time = Eroot.findall('System')[0].find('TimeCreated').attrib['SystemTime']
            # 详细数据
            Datas = Eroot.findall('EventData')[0].findall('Data')
            # print(type(time))
            #ip地址
            # ip=re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', Datas)

            # 匹配 账号登陆成功的事件信息 - 4624
            if EventID == "4624":
                # 输出事件时间、时间ID、计算机名称
                print(time,EventID,Computer)
                # 输出遍历数据
                for data in Datas:
                    print(data.get("Name"),data.text)

                    # print("+++++++++++++++++++++++++++++++++++")
                        # print(data.get("IpAddress"), data.text)
                print("-----------------")


