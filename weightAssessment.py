'''
这是加权打分的文件
'''
#基于主机的加权打分，根据多个eventid判断主机是否受攻击

class weightAsses:

    def __init__(self,weight):
        self.weight=0.00

    def modifyWeight(self,weightChange):
        '''
        weight可以为正可以为负
        :param weight:
        :return:
        '''
        self.weight+=weightChange



#基于



