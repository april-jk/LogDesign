import  socket
import core.encode.AES
key='23dc31mceow3ewCD214mEc2094MEEwqw'
# 创建套接字
tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 绑定信息
tcp_server_socket.bind(("127.0.0.1", 7878))
# 使用socket创建的套接字默认的属性是主动的，使用listen变为被动，就可以接收别人的链接
tcp_server_socket.listen(128)
while 1:
    # 如果有新的客户端来链接服务器，那么就产生一个新的套接字专门为这个客户端服务
    # client_socket 用来为这个客户端服务
    # tcp_server_socket 就可以省下来专门等待其他新客户端的链接
    client_socket, clientAddr = tcp_server_socket.accept()
    # 接受对方发过来的数据
    recv_data = client_socket.recv(1024)
    data=recv_data.decode('gbk')
    print('接收到的原始数据：', data)
    data= core.encode.AES.decrypt(data, key)
    print('解密后数据：',data)

    # 发送一些数据到客户端
    client_socket.send("成功接收数据，请知悉".encode('gbk'))
# 关闭客户端服务的套接字
client_socket.close()


