import json

from flaskBak.sql.login import loginVerify
def loginVerify_api(uname,passwd):
    uname=str(uname)
    passwd=str(passwd)
    result=json.dumps(loginVerify(uname,passwd))
    return result
    '''
    :param uname:
    :param passwd:
    :return: 验证成功返回OK，验证失败返回NO
    '''

if __name__ == '__main__':
    print(loginVerify('admin','admin'))