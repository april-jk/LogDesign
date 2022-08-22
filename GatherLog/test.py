import socket


"""将路径文件使用字节流增量读入"""
"""增量读入"""
"""
fp = open("D:/b.txt", mode="rb")
data=fp.read()
print(data)
"""


print("\n*****************")

fd=open("C:/Users/76708/Desktop/111/c.txt",'rb') #获得一个句柄
for i in range(1): #读取三行数据
    data=fd.readline()
    print(data)
    label=fd.tell() #记录读取到的位置
fd.close() #关闭文件
""""""

#再次阅读文件
while True:
    fd = open("C:/Users/76708/Desktop/111/c.txt", 'rb')  # 获得一个句柄
    fd.seek(label, 0)  # 把文件读取指针移动到之前记录的位置
    data=fd.readline()  # 接着上次的位置继续向下读取
    label = fd.tell()
    if data!=b'':
        print(data)
        label = fd.tell()
        print(label)
    fd.close()
