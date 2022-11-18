def loginVerify(uname,passwd):
    uname=str(uname)
    passwd=str(passwd)
    if uname=='admin' and passwd=='admin':
        return 'OK'
    else:
        return 'NO'