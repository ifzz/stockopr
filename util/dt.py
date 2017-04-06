#-*- encoding: utf-8 -*-

import time
import datetime

'''
一、休市安排
　　（一）元旦：1月1日（星期五）至1月3日（星期日）休市，1月4日（星期一）起照常开市。
　　（二）春节：2月7日（星期日）至2月13日（星期六）休市，2月15日（星期一）起照常开市。另外，2月6日（星期六）、2月14日（星期日）为周末休市。
　　（三）清明节：4月2日（星期六）至4月4日（星期一）休市，4月5日（星期二）起照常开市。
　　（四）劳动节：4月30日（星期六）至5月2日（星期一）休市，5月3日（星期二）起照常开市。
　　（五）端午节：6月9日（星期四）至6月11日（星期六）休市，6月13日（星期一）起照常开市。另外，6月12日（星期日）为周末休市。
　　（六）中秋节：9月15日（星期四）至9月17日（星期六）休市，9月19日（星期一）起照常开市。另外，9月18日（星期日）为周末休市。
　　（七）国庆节：10月1日（星期六）至10月7日（星期五）休市，10月10日（星期一）起照常开市。另外，10月8日（星期六）、10月9日（星期日）为周末休
'''

holiday_str=["1-1", "2-8", "2-9", "2-10", "2-11", "2-12", "4-4", "5-2", "6-9", "6-10", "9-15", "9-16", "10-3", "10-4", "10-5", "10-6", "10-7",]
holiday_str="1-1, 2-8, 2-9, 2-10, 2-11, 2-12, 4-4, 5-2, 6-9, 6-10, 9-15, 9-16, 10-3, 10-4, 10-5, 10-6, 10-7,"
lastday = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

def mktime(_datetime):
    # time.mktime((tm_today.tm_year, tm_today.tm_mon, tm_today.tm_mday, 9, 30, 0, 0, 0, 0))
    return int(time.mktime(_datetime.timetuple()))

today = datetime.date.today()
start_time_am = mktime(datetime.datetime(today.year, today.month, today.day, 9, 30))
end_time_pm = mktime(datetime.datetime(today.year, today.month, today.day, 15))
end_time_day = mktime(datetime.datetime(today.year, today.month, today.day, 23, 59, 59))

def set_today():
    global today
    today = datetime.date.today()

def set_trade_time():
    global start_time_am
    global end_time_pm
    global end_time_day
    start_time_am = mktime(datetime.datetime(today.year, today.month, today.day, 9, 30))
    end_time_pm = mktime(datetime.datetime(today.year, today.month, today.day, 15))
    end_time_day = mktime(datetime.datetime(today.year, today.month, today.day, 23, 59, 59))


#day_str: 2016-1-17
def isholiday(day=None) :
    if not day:
        day = today
    day_str = '%d-%d,' % (day.month, day.day)
    if holiday_str.find(day_str) >= 0:
        return True
    return False

def isweedend(day=None):
    if not day:
        day = today

    #weekday = date.isoweekday(date.today()) #weekday is not ok...
    weekday = date.isoweekday(day) #date.isoweekday(datetime.date(2015, 4, 16))
    if weekday % 7 == 0 or weekday == 6: #Sunday is 7...
        return True
    return False
    #if tm_day.tm_wday == 0 or tm_day.tm_wday == 6: #why? why? Mon. -> Sun.
    #    return True
    #return False

def istradeday(day=None):
    if not day:
        day = today

    if isweedend(day) or isholiday(day):
        return False
    return True


def istradetime():
    if not istradeday(today):
        return False

    now = time.time()
    if now < start_time_am or now > end_time_pm:
        return False

    if now > start_time_am + 2 * 3600 and now < end_time_pm - 2 * 3600:
        return False

    return True

def sumofweektradeday(day):
    sum = 0
    year = day.year
    mon = day.month
    day = day.day
    if mon == 2 and year % 4 == 0: #
        lastday[1] = 29
    for d in range(day, lastday[mon - 1] + 1):
        day_str = [0, 0, 0]
        day_str[0] = year
        day_str[1] = mon
        day_str[2] = d
        #mktime(tm_day)
        if isweedend(day_str):
            break
        if isholiday(day_str):
            continue
        sum += 1
    #tm_day.tm_mday = day #
    return sum

def sumofmonthtradeday(day): #tm_day, is str
    sum = 0
    year = day.year
    mon = day.month
    day = day.day
    lastday_tmp = lastday[mon - 1] + 1
    if mon == 2 and year % 4 == 0: #ÔÂ·ÝŽÓ1ÔÂ¿ªÊŒ, Äê·ÝÎªÊµŒÊÄê·Ý, ²»ÓÃŒÓ1900
        lastday_tmp = 29 #È«ŸÖ±äÁ¿!!!
    for d in range(day, lastday_tmp):
        day_str = [0, 0, 0]
        day_str[0] = year
        day_str[1] = mon
        day_str[2] = d
        #mktime(tm_day)
        if istradeday(day_str):
            sum += 1
    #tm_day.tm_mday = day #
    return sum
tm_day = time.localtime()

def sumofyeartradeday(y):
    days = 0
    for m in range(1, 13):
        day = date(y, m, 1)
        days += sumofmonthtradeday(day)
    return days

def dt64_to_dt(dt64):
    return dt64.astype('M8[D]').astype('O')  #'M8[ms]'
