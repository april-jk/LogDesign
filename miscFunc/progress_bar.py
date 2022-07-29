import sys
import time

def progress_bar(percentage):
    '''
    会在终端产生进度条
    :param percentage: 一个0-1的实数
    :return: 无
    '''
    percentage = int(percentage * 100)
    print("\r", end="")
    print("[*]Progress: {}%: ".format(percentage), "▋" * (percentage // 2), end="")
    sys.stdout.flush()

if __name__ == '__main__':
    progress_bar()