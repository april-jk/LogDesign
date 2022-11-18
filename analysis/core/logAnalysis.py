import pickle
from analysis.core.dataStruct.dataStruct import attactEvent_2425

f = open('../../pklFile/test_all.pkl', 'rb')
df = pickle.load(f)
f.close()

# print(list4624_4625.values[0][1])
# for data in list4624_4625.index:
#     print(data.loc[list4624_4625].values, data.loc[list4624_4625].values[0], data.loc[list4624_4625].values[1])

# def findEnumerationCrackRDP(list4624_4625):
'''
    爆破检测函数
'''
lastTime='2002-04-11 05:21:00'
# count_Attact=0
AttactList=[]
waring=[]
def getEventIndex(ip,ipList):
    for n,i in enumerate(ipList,0):
        if i.ip==ip:
            return n

def inIpList(ip,List):
    for i in List:
        if i.ip==ip:
            return True
    return False
def inuidList(uid,List):
    for i in List:
        if i.uid==uid:
            return True
    return False
def inLogonTypeList(logontype,List):
    for i in List:
        if i.logontype==logontype:
            return True
    return False

def id4624(data):
    if data[2] == '4624':
        for i in AttactList:
            for j in waring:
                if data[29] == j:
                    return
            if data[29] == i.ip and data[7] == 'ANONYMOUS LOGON':
                waring.append(data[29])
                print("hacked through ANONYMOUS LOGON attact!ip:【 " + i.ip+' 】')
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
                event = attactEvent_2425(data[1],data[20], data[29],data[16])
                # temp1 = data[29]
                AttactList.append(event)
        elif inuidList(data[16], AttactList):
            index = getEventIndex(data[29], AttactList)
            AttactList[index].appendTime(data[1])
        elif inLogonTypeList(data[20], AttactList):
            if data[29] != '':
                event = attactEvent_2425(data[1], data[20], data[29],data[16])
                # temp1 = data[29]
                AttactList.append(event)
        else:
            if data[29] != '':
                event = attactEvent_2425(data[1], data[20], data[29],data[16])
                # temp1 = data[29]
                AttactList.append(event)
                '''
                16是uid
                29是logontype
                '''
def id4729(data):
    '''
    :param data:
    :return: 创建的隐藏用户的用户名
    '''
    if data[2] == '4720':
        TargetUserName=data[7]#根据这个用户名继续后续操作
        return TargetUserName
        '''
        用户创建
        TargetUserName 为创建的用户名
        根据隐藏加权
        '''

def addGroup(data):
    if data[2] == '4728' or data[2] == '4732' or data[2] == '4756':
        # for i in AttactList:
            # if data[16]==i.uid:
            #     print("find GroupAdded !")
        TargetUserName=data[7]
        return TargetUserName
        '''
        用户被添加到安全组
        TargetUserName是添加的目的组，piao$添加到administrators产生的ID为4732
                                    更改Administrator对注册表完全控制权限产生4728
        '''
def removeGroup(data):
    if data[2] == '4729' or data[2] == '4733' or data[2] == '4757':
        '''
        用户被从安全组移除
        '''
def id4719(data):
    if data[2] == '4719':
        '''
        系统审核策略已更改
        '''
def id4672(data):
    if data[2] == '4672':
        '''
        分配给新登录的特殊权限
        '''
def id4723_24(data):
    '''
    4723是更改用户密码
    4724是设置用户密码
    :param data:
    :return:
    '''

'''
4798?
'''
def generatIPList():
    for data in df.values:
        # print(data[1]) #2022-04-18 20:11:53
        '''
        4624.4625都是29
        '''

        id4625(data)
        id4624(data)
        # if data[16]=='S-1-5-21-1390822584-1902517743-2670227040-500':
        #     #adminsitrator
        #     print(data)




    return AttactList

def findCleanUP(data):
    '''
    日志清除行为发现
    :return:存在1102返回True
            不存在返回False
    '''
    if data[2]=='1102':
        return True
    else:
        return False

ip=generatIPList()






'''
#显示所有列
pd.set_option('display.max_columns', None)
#显示所有行
pd.set_option('display.max_rows',None)

下面三行查看dataframe的数据结构信息（列名）
c = list4624_4625.dtypes
for i in c.index: # 依次选取Series的各个key
    print(i,'   ',c[i]) # 这里的c[i]的使用，在Series中可以使用Series[key]的形式取出对应的value
'''

