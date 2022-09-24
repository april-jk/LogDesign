import json

from flaskBak.sql.hostCount import getLogNumber,getHostNumber,getWarnNumber,getWeakNumber

def getLogNumber_api():
    num=json.dumps(getLogNumber())
    return num

def getWarnNumber_api():
    num=json.dumps(getWarnNumber())
    return num


def getWeakNumber_api():
    num=json.dumps(getWeakNumber())
    return num


def getHostNumber_api():
    num=json.dumps(getHostNumber())
    return num


