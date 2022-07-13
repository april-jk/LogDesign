# -*- coding: utf-8 -*-

'''获取当前日期前后N天或N月的日期'''

from time import strftime, localtime
from datetime import timedelta, date
import calendar

year = strftime("%Y", localtime())
mon = strftime("%m", localtime())
day = strftime("%d", localtime())
hour = strftime("%H", localtime())
min = strftime("%M", localtime())
sec = strftime("%S", localtime())
a=localtime()


def formerIsLater(time1,time2,ignore):
    '''
    MODIFIED!
    :param time1: 第一个时间
    :param time2: 第二个时间，如果第一个时间更大（后发生），返回True
    :param ignore: 如果为True，直接返回True，用于全日志分析
    :return: True/False
    '''
    time1=int(datetimestr(time1))
    time2=int(datetimestr(time2))
    if ignore==True:
        return True
    else:
        if time1 - time2 >= 0:
            return True
        else:
            return False


def today():
    '''''
    get today,date format="YYYY-MM-DD"
    '''''
    return date.today()


def todaystr():
    '''
    get date string, date format="YYYYMMDD"
    '''
    return year + mon + day


def datetime():
    '''''
    get datetime,format="YYYY-MM-DD HH:MM:SS"
    '''
    return strftime("%Y-%m-%d %H:%M:%S", localtime())


def datetimestr(date):
    '''''
    MODIFIED!
    get datetime string
    :param date:2022-04-14 22:34:53
    :return 20220414
    '''
    #日志时间格式：2022-04-14 22:34:53
    k=date.index(' ')
    date=date[:k]
    i=date.index('-')
    year=date[:i]
    j=date.rindex('-')
    month=date[i+1:j]
    day=date[j+1:]
    return year+month+day


def get_day_of_day(n=0):
    '''''
    if n>=0,date is larger than today
    if n<0,date is less than today
    date format = "YYYY-MM-DD"
    '''
    if (n < 0):
        n = abs(n)
        return date.today() - timedelta(days=n)
    else:
        return date.today() + timedelta(days=n)


def get_days_of_month(year, mon):
    '''''
    get days of month
    '''
    return calendar.monthrange(year, mon)[1]


def get_firstday_of_month(year, mon):
    '''''
    get the first day of month
    date format = "YYYY-MM-DD"
    '''
    days = "01"
    if (int(mon) < 10):
        mon = "0" + str(int(mon))
    arr = (year, mon, days)
    return "-".join("%s" % i for i in arr)


def get_lastday_of_month(year, mon):
    '''''
    get the last day of month
    date format = "YYYY-MM-DD"
    '''
    days = calendar.monthrange(year, mon)[1]
    mon = addzero(mon)
    arr = (year, mon, days)
    return "-".join("%s" % i for i in arr)


def get_firstday_month(n=0):
    '''''
    get the first day of month from today
    n is how many months
    '''
    (y, m, d) = getyearandmonth(n)
    d = "01"
    arr = (y, m, d)
    return "-".join("%s" % i for i in arr)


def get_lastday_month(n=0):
    '''''
    get the last day of month from today
    n is how many months
    '''
    return "-".join("%s" % i for i in getyearandmonth(n))


def getyearandmonth(n=0):
    '''''
    get the year,month,days from today
    befor or after n months
    '''
    thisyear = int(year)
    thismon = int(mon)
    totalmon = thismon + n
    if (n >= 0):
        if (totalmon <= 12):
            days = str(get_days_of_month(thisyear, totalmon))
            totalmon = addzero(totalmon)
            return (year, totalmon, days)
        else:
            i = totalmon / 12
            j = totalmon % 12
            if (j == 0):
                i -= 1
                j = 12
            thisyear += i
            days = str(get_days_of_month(thisyear, j))
            j = addzero(j)
            return (str(thisyear), str(j), days)
    else:
        if ((totalmon > 0) and (totalmon < 12)):
            days = str(get_days_of_month(thisyear, totalmon))
            totalmon = addzero(totalmon)
            return (year, totalmon, days)
        else:
            i = totalmon / 12
            j = totalmon % 12
            if (j == 0):
                i -= 1
                j = 12
            thisyear += i
            days = str(get_days_of_month(thisyear, j))
            j = addzero(j)
            return (str(thisyear), str(j), days)


def addzero(n):
    '''''
    add 0 before 0-9
    return 01-09
    '''
    nabs = abs(int(n))
    if (nabs < 10):
        return "0" + str(nabs)
    else:
        return nabs


def get_today_month(n=0):
    '''''
    获取当前日期前后N月的日期
    if n>0, 获取当前日期前N月的日期
    if n<0, 获取当前日期后N月的日期
    date format = "YYYY-MM-DD"
    '''
    (y, m, d) = getyearandmonth(n)
    arr = (y, m, d)
    if (int(day) < int(d)):
        arr = (y, m, day)
    return "-".join("%s" % i for i in arr)


if __name__ == "__main__":
    print(today())
    print(todaystr())
    print(datetime())
    # print(datetimestr())
    print(get_day_of_day(20))
    print(get_day_of_day(-3))
    print(get_today_month(-3))
    print(get_today_month(3))
    print(datetimestr('2022-04-14 22:34:53'))