import pickle
from dataStruct import attactEvent_2425

f = open('../pklFile/test_ini.pkl', 'rb')
df = pickle.load(f)
f.close()


list4624_4625=df[0]
# print(list4624_4625.values[0][1])
# for data in list4624_4625.index:
#     print(data.loc[list4624_4625].values, data.loc[list4624_4625].values[0], data.loc[list4624_4625].values[1])

# def findEnumerationCrackRDP(list4624_4625):
'''
    爆破检测函数
'''
lastTime='2002-04-11 05:21:00'
count_Attact=0
ipList=[]
def getEventIndex(ip,ipList):
    for n,i in enumerate(ipList,0):
        if i.ip==ip:
            return n

    # for i in ipList:
    #     if i.ip==ip:
    #         break
    # return i.index
def inIpList(ip,ipList):
    for i in ipList:
        if i.ip==ip:
            return True
    return False

def generatIPList():
    for data in list4624_4625.values:
        # print(data[1]) #2022-04-18 20:11:53
        '''
        4624.4625都是29
        '''
        if data[2] == '4625':
            if not inIpList(data[29], ipList):
                event = attactEvent_2425(data[1], '4625', data[29])
                temp1 = data[29]
                ipList.append(event)
            else:
                index = getEventIndex(data[29], ipList)
                ipList[index].appendTime(data[1])

        if data[2] == '4624':
            for i in ipList:
                if data[29] == i.ip:
                    print("attact!ip:" + i.ip)
                    '''
                    这里要考虑一下后面怎么接口化
                    '''
                    break
    return ipList

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

