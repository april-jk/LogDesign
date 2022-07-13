import pickle

f = open('../pklFile/test_ini.pkl', 'rb')
df = pickle.load(f)
f.close()


list4624_4625=df[1]
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
def inIpList(ip,ipList):
    for i in ipList:
        if i==ip:
            return True
    return False

for data in list4624_4625.values:
    # print(data[1]) #2022-04-18 20:11:53
    '''
    4624.4625都是29
    '''
    if data[2]=='4625':
        if not inIpList(data[29],ipList):
            ipList.append(data[29])


    if data[2]=='4624':
        for i in ipList:
            if data[29] == i:
                print("attact!ip:"+i)






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

