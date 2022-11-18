import json

from flaskBak.sql.host import getLogNumber,getHostNumber,getWarnNumber,getWeakNumber

def getNumber_api():
    test=[{'logNum':0,'warnNum':0,'weakNum':0,'HostNum':0}]
    test['logNum']=getLogNumber_api()
    test['warnNum']=getWarnNumber_api()
    test['weakNum']=getWeakNumber_api()
    test['HostNum']=getHostNumber_api()
    # num.append(getLogNumber())
    num=json.dumps(test)
    return num

def getLogNumber_api():
    num=getLogNumber()
    return num

def getWarnNumber_api():
    # num=getWarnNumber()
    return 25


def getWeakNumber_api():
    # num=getWeakNumber()
    return 2


def getHostNumber_api():
    num=getHostNumber()
    return num

def getDashList():
    dashlist=[{'name':'testlog','ipaddr':'10.10.100.1','group':'local','registed':'yes','lastModify':'2022-08-10 20:12:43'},
              {'name':'win11-yoga-10.10.101.3','ipaddr':'10.10.101.3','group':'local','registed':'yes','lastModify':'2022-09-03 23:11:49'},
              {'name':'winserver2010-10.1.1.12','ipaddr':'10.1.1.12','group':'local','registed':'yes','lastModify':'2022-09-18 20:54:23'}]
    return json.dumps(dashlist)



if __name__ == '__main__':
    # print(getNumber_api())
    print(getDashList())