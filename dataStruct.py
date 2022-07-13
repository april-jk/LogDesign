class attactEvent_2425:
    '所有攻击事件的基类'
    Count = 0#这是全部有多少个此类的对象

    def __init__(self,time,LogonType,ip,uid,Count=Count):
        self.time=[]
        self.time.append(time)
        self.ip = ip
        self.LogonType=LogonType
        self.count=1
        attactEvent_2425.Count += 1
        self.uid=uid

    def appendTime(self, time):
        self.time.append(time)
        self.count=self.count+1


class ANONYMOUS_LOGON:
    Count=0

    def __init__(self,time,LogonType,ip,Count=Count):
        self.time = []
        self.time.append(time)
        self.ip = ip
        self.LogonType = LogonType
        self.count = 1
        attactEvent_2425.Count += 1

    def append(self,time):
        self.time.append(time)
        self.count=self.count+1