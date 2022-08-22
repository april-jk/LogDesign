import socket
from Crypto.Cipher import AES

port = 7878
host = '127.0.0.1'
data = ''
key='23dc31mceow3ewCD214mEc2094MEEwqw'
'''
下一步这里实现先交互认证码，然后密钥交互
'''
def socketClient(host,port,data):
    client_socket = socket.socket()
    client_socket.connect((host, port))

    try:
        data= AES.encrypt(data, key)
        data = data.encode()
        client_socket.send(data)
        response = client_socket.recv(1024)
        response = response.decode()
        print(response)
    except:
        print('')

    client_socket.close()



while 1:
    """将路径文件使用字节流增量读入"""

    fd = open("C:/Users/76708/Desktop/111/c.txt", 'rb')  # 获得一个句柄
    for i in range(1):  # 读取数据
        data = fd.readline()
        print(data)
        label = fd.tell()  # 记录读取到的位置
    fd.close()  # 关闭文件

    while True:
        fd = open("C:/Users/76708/Desktop/111/c.txt", 'rb')  # 获得一个句柄
        fd.seek(label, 0)  # 把文件读取指针移动到之前记录的位置
        data = fd.readline()  # 接着上次的位置继续向下读取
        label = fd.tell()
        if data != b'':
            socketClient(host, port, data)
            label = fd.tell()
            print(label)
        fd.close()



