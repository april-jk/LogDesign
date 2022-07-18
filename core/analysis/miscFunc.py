
def getEventIndex(ip, ipList):
    for n, i in enumerate(ipList, 0):
        if i.ip == ip:
            return n


def inIpList(ip, List):
    for i in List:
        if i.ip == ip:
            return True
    return False


def inuidList(uid, List):
    for i in List:
        if i.uid == uid:
            return True
    return False


def inLogonTypeList(logontype, List):
    for i in List:
        if i.logontype == logontype:
            return True
    return False
