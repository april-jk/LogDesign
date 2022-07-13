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
                content_list = []
                list4624_4625= []
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
                #根据eventID来分别存储
                    #4624登陆成功,4625登陆失败
                    if content_dict['EventID'] == '4624' :
                    #if content_dict['EventID'] == '4624' and 'TargetUserName_EventData' != 'SYSTEM':
                    # if content_dict['EventID'] == '4624' and content_dict['LogonType_EventData']=='10':
                    # if content_dict['EventID'] == '4624':
                        # list4624_4625.append(content_dict)
                    # if content_dict['EventID']=='5158':
                    #     f=open('./tmp_txt/4624-4625Log.txt','a')
                    #     f.write(str(content_dict))
                    #     f.write('\n')

                    # print(type(content_dict))
                        try:
                            print(content_dict)
                        except:
                            continue

                    # if content_dict['EventID']=='4720':

                        # 归档日志信息
                    # content_list.append(content_dict)
                    # 现在evtx节点的信息获取已经完成
                    # print(content_list)
        # all_log = DataFrame(content_list).fillna('')  # 让 Nan 为空字符串
        # all_log = DataFrame(content_list).fillna('').sort_values(by=['SystemTime'])   # 按时间排序
        # list4624_4625=DataFrame(content_list).fillna('')
        # list4624_4625=DataFrame(content_list).fillna('').sort_values(by=['SystemTime'])
        # f = open('./pklFile/test_ini.pkl', 'wb')
        # pickle.dump([all_log,list4624_4625], f)
        # f.close()
        # return all_log
    # 出现一些编码无法识别的日志文件，如果该日志不属于 ['Security', 'System', 'Setup']，则进行忽略
    except (Evtx.BinaryParser.OverrunBufferException, KeyError):
        if os.path.splitext(os.path.basename(evtxpath))[0] not in ['Security', 'System', 'Setup']:
            return DataFrame()
        else:
            raise


#Log_Get('./Winlog/yoga/Security.evtx')
# Log_Get('./Winlog/server2012/RDP_securityLog.evtx')
Log_Get('./Winlog/server2012/server.evtx')


'''
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:34:53', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14'【9】, 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3'【20】, 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '81.68.184.140', 'IpPort_EventData': '0'}
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:35:30', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14', 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3', 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '36.138.82.9', 'IpPort_EventData': '0'}
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:35:40', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14', 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3', 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '81.70.13.118', 'IpPort_EventData': '0'}
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:36:08', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14', 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3', 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '119.29.73.165', 'IpPort_EventData': '0'}
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:37:55', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14', 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3', 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '81.70.13.118', 'IpPort_EventData': '0'}
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:40:09', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14', 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3', 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '81.70.13.118', 'IpPort_EventData': '0'}
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:42:24', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14', 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3', 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '81.70.13.118', 'IpPort_EventData': '0'}
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:42:30', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14', 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3', 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '36.138.82.9', 'IpPort_EventData': '0'}
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:44:38', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14', 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3', 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '81.70.13.118', 'IpPort_EventData': '0'}
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:46:54', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14', 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3', 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '81.70.13.118', 'IpPort_EventData': '0'}
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:47:48', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14', 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3', 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '81.68.248.12', 'IpPort_EventData': '0'}
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:48:00', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14', 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3', 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '42.192.53.251', 'IpPort_EventData': '0'}
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:49:08', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14', 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3', 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '81.70.13.118', 'IpPort_EventData': '0'}
{'Channel': 'Security', 'SystemTime': '2022-04-14 22:49:27', 'EventID': '4625', 'Level': '0', 'UserID': '', 'ProcessID': '660', 'Computer': '10_0_12_14', 'SubjectUserSid_EventData': 'S-1-0-0', 'SubjectUserName_EventData': '-', 'SubjectDomainName_EventData': '-', 'SubjectLogonId_EventData': '0x0000000000000000', 'TargetUserSid_EventData': 'S-1-0-0', 'TargetUserName_EventData': 'ADMINISTRATOR', 'Status_EventData': '0xc000006d', 'FailureReason_EventData': '%%2313', 'SubStatus_EventData': '0xc000006a', 'LogonType_EventData': '3', 'LogonProcessName_EventData': 'NtLmSsp ', 'AuthenticationPackageName_EventData': 'NTLM', 'WorkstationName_EventData': '-', 'TransmittedServices_EventData': '-', 'LmPackageName_EventData': '-', 'KeyLength_EventData': '0', 'ProcessId_EventData': '0x0000000000000000', 'ProcessName_EventData': '-', 'IpAddress_EventData': '36.138.82.9', 'IpPort_EventData': '0'}
'''