import socket
import core.encode.AES
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
        data= core.encode.AES.encrypt(data, key)
        data = data.encode()
        client_socket.send(data)
        response = client_socket.recv(1024)
        response = response.decode()
        print(response)
    except:
        print('')

    client_socket.close()

while 1:
    data=input()
    socketClient(host,port,data)


