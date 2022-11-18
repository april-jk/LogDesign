import re
import sys
from collections import Counter
from prettytable import PrettyTable

# 获取文件名
filename = sys.argv[1]

success_record = []
failed_record = []
success_ip = []
failed_ip = []
month = {"Jan": "一月", "Feb": "二月", "Mar": "三月", "Apr": "四月", "May": "五月", "Jun": "六月", "Jul": "七月",
         "Aug": "八月", "Sept": "九月", "Oct": "十月", "Nov": "十一月", "Dec": "十二月"}


def search():
    global success_record, failed_record, filename  # 全局变量
    pattern = re.compile(r'(.*?) (\d+) (.*?) .*?: (.*?) password for (.*?) from (.*?) port (\d+)')  # 正则规则
    file = open(filename, 'r')  # 打开文件
    for i in file:
        check_login = pattern.search(i)  # 正则匹配
        if check_login:  # 检查是否匹配到内容，如果没有就下一条
            if check_login.group(4) == "Accepted":  # 成功登录
                # 这里的.group(0)是原文，.group(1、2、3)均为日期，.group(5)为用户名,6是登录的IP地址，.group(7)为对方的端口
                success_record.append(
                    [check_login.group(1), check_login.group(2), check_login.group(3), check_login.group(5),
                     check_login.group(6), check_login.group(7)])
            elif check_login.group(4) == "Failed":  # 失败登录
                if "invalid user" in check_login.group(5):  # 用户名会因为黑客测试无效用户而变得多余，所以删掉多余的部分
                    failed_record.append(
                        [check_login.group(1), check_login.group(2), check_login.group(3), check_login.group(5)[13:],
                         check_login.group(6), check_login.group(7)])
                else:
                    failed_record.append(
                        [check_login.group(1), check_login.group(2), check_login.group(3), check_login.group(5),
                         check_login.group(6), check_login.group(7)])
        else:
            continue


def intrusion_detection(wfile, success_ip, failed_ip, fdst):
    check_result = set(success_ip).intersection(set(failed_ip))  # 查看成功的IP和失败的IP中是否有交集，检查是否爆破成功
    if check_result:
        print("\n[+]入侵检测:")
        wfile.write("\n[+]入侵检测: \n")
        prcheck = PrettyTable(field_names=["登录IP", "结果", "原因"])
        for i in check_result:
            if int(fdst[i]) > 5:
                prcheck.add_row([i, "成功", "该IP进行密码爆破，猜解到成功的密码后，登录了系统...$result1"])
                wfile.write("  检测到IP：" + str(i) + " 爆破成功\n")
            else:
                wfile.write("  检测到IP：" + str(i) + " 可疑,请核实\n")
                prcheck.add_row([i, "可疑", "该IP已登录过系统，但是因为次数过少不像是暴力破解，请核实...$result2"])
        print(prcheck)
    else:
        print("\n[-]未发现有可疑|成功事件$result3\n")


def writeANDprint_data(month, filename, success_ip, failed_ip):
    global success_record, failed_record
    wfile = open("result.txt", "w")
    wfile.write("分析文件：" + filename + "\n")
    if success_record:  # 先判断是否存在内容
        sc_result = PrettyTable(field_names=["登录时间", "用户名", "登录IP", "连接端口", "结果"])
        wfile.write("[+] 已找到成功的记录" + str(len(success_record)) + "条\n")
        print("[+] 已找到成功的记录" + str(len(success_record)) + "条")
        for i in success_record:
            sc_result.add_row([month[i[0].rstrip()] + i[1] + "号 " + i[2], i[3], i[4], i[5], "成功"])
            wfile.write(
                "        登录时间: " + month[i[0].rstrip()] + i[1] + "号 " + i[2] + " 用户名: " + i[3] + " 登录IP: " +
                i[4] + " 连接端口: " + i[5] + "\n")
            success_ip.append(i[4])
        print(sc_result)
    else:
        print("[-] 无SSH登录成功的记录...")
        wfile.write("[-] 无SSH登录成功的记录...\n")
    if len(failed_record) > 10:
        print("[+]数目超过10条，不予显示...请前往文件中查看....\n")
        wfile.write("\n[+] 已找到失败的记录" + str(len(failed_record)) + "条\n")
        for i in failed_record:
            wfile.write(
                "        登录时间: " + month[i[0].rstrip()] + i[1] + "号 " + i[2] + " 用户名: " + i[3] + " 登录IP: " +
                i[4] + " 连接端口: " + i[5] + "\n")
            failed_ip.append(i[4])
    elif len(failed_record) <= 10:
        print("\n[+] 已找到失败的记录" + str(len(failed_record)) + "条")
        wfile.write("\n[+] 已找到失败的记录" + str(len(failed_record)) + "条\n")
        fa_result = PrettyTable(field_names=["登录时间", "用户名", "登录IP", "连接端口", "结果"])
        for i in failed_record:
            fa_result.add_row([month[i[0].rstrip()] + i[1] + "号 " + i[2], i[3], i[4], i[5], "失败"])
            wfile.write(
                "        登录时间: " + month[i[0].rstrip()] + i[1] + "号 " + i[2] + " 用户名: " + i[3] + " 登录IP: " +
                i[4] + " 连接端口: " + i[5] + "\n")
            failed_ip.append(i[4])
        print(fa_result)
    else:
        print("\n[-] 无SSH登录失败的记录...")
        wfile.write("\n[-] 无SSH登录失败的记录...\n")
    scst = Counter(success_ip)
    fdst = Counter(failed_ip)
    wfile.write("\n[+]结果统计：\n  成功的记录统计：\n")
    print("[+]结果统计：\n  成功的记录统计：")
    sc_ip = PrettyTable(field_names=["登录IP", "统计次数"])
    for i in scst.keys():
        # print("    IP地址: "+i+" 找到的记录有"+str(scst[i])+"次")
        sc_ip.add_row([i, str(scst[i])])
        wfile.write("    IP地址: " + i + " 找到的记录有" + str(scst[i]) + "次\n")
    print(sc_ip)
    wfile.write("  失败的记录统计：\n")

    print("  失败的记录统计：")
    fa_ip = PrettyTable(field_names=["登录IP", "统计次数"])
    for i in fdst.keys():
        # print("    IP地址: "+i+" 找到的记录有"+str(fdst[i])+"次")
        fa_ip.add_row([i, str(fdst[i])])
        wfile.write("    IP地址: " + i + " 找到的记录有" + str(fdst[i]) + "次\n")
    print(fa_ip)
    intrusion_detection(wfile, success_ip, failed_ip, fdst)
    wfile.close


search()
writeANDprint_data(month, filename, success_ip, failed_ip)