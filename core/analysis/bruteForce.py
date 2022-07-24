from core.dataStruct.dataStruct import attactEvent_2425
from core.analysis.miscFunc import inIpList, inLogonTypeList, getEventIndex, inuidList

AttactList = []
waring=[]

def id4624(data):
    if data[2] == '4624':
        for i in AttactList:
            for j in waring:
                if data[29] == j:
                    return
            if data[29] == i.ip and data[7] == 'ANONYMOUS LOGON':
                waring.append(data[29])
                print("hacked through ANONYMOUS LOGON attact!ip:【 " + i.ip + ' 】')
            elif data[29] == i.ip:
                waring.append(data[29])
                print("存在爆破成功事件！ attact!ip:" + i.ip)
                break
                '''
                WorkstationName_EventData是登陆的主机的名字（攻击者） 结合这个和ip地址归类
                '''


def id4625(data):
    if data[2] == '4625':
        if not inIpList(data[29], AttactList):
            if data[29] != '':
                event = attactEvent_2425(data[1], data[20], data[29], data[16])
                # temp1 = data[29]
                AttactList.append(event)
        elif inuidList(data[16], AttactList):
            index = getEventIndex(data[29], AttactList)
            AttactList[index].appendTime(data[1])
        elif inLogonTypeList(data[20], AttactList):
            if data[29] != '':
                event = attactEvent_2425(data[1], data[20], data[29], data[16])
                # temp1 = data[29]
                AttactList.append(event)
        else:
            if data[29] != '':
                event = attactEvent_2425(data[1], data[20], data[29], data[16])
                # temp1 = data[29]
                AttactList.append(event)
                '''
                16是uid
                29是logontype
                '''
def findInBruteForce(data):
    id4625(data)
    id4624(data)