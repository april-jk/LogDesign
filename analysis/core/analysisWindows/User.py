# from core.analysisWindows.miscFunc import


#userAdd
def id4720(data):
    if data[2] == '4720':
        TargetUserName=data[7]#根据这个用户名继续后续操作
        return TargetUserName

#userDel
def id4726(data):
    if data[2]=='4726':
        '''
        4726是用户删除
        :param data:
        :return: 进行此操作的用户
        '''
        TargetUserName = data[7]  # 根据这个用户名继续后续操作
        return TargetUserName
def changepasswd(data):
    '''
        4723是更改用户密码
        4724是设置用户密码
        subjectUserName是用户名 11 可以知道是哪个用户在进行此操作
    :param data:
    :return: 进行此操作的用户
    '''
    if data[2]=='4723':
        return data[11]
    if data[2]=='4724':
        return data[11]

def findInUser(data):
    id4726(data)
    id4720(data)
    changepasswd(data)


