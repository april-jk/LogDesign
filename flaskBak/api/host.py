import json

from flaskBak.sql.host import getHostList


def getHostList_api():
    dashlist = [{'name': 'testlog', 'ipaddr': '10.10.100.1', 'group': 'local',
                 'lastModify': '2022-08-10 20:12:43','type':'Windows'},
                {'name': 'win11-yoga-10.10.101.3', 'ipaddr': '10.10.101.3', 'group': 'local',
                 'lastModify': '2022-09-03 23:11:49','type':'Windows'},
                {'name': 'winserver2010-10.1.1.12', 'ipaddr': '10.1.1.12', 'group': 'local',
                 'lastModify': '2022-09-18 20:54:23','type':'Windows'}]
    return json.dumps(dashlist)

def getHostList_easy_api():
    list=getHostList()
    list=json.dumps(list)
    return list

if __name__ == '__main__':
    print(getHostList_easy_api())