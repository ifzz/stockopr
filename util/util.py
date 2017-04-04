import psutil
import datetime
import time

def get_pname_by_id(pid):
    try:
        p = psutil.Process(pid)
        return p.name()
    except psutil.NoSuchProcess:
        return None

def get_pid_by_name(pname):
    """ get process by name
    return the first process if there are more than one
    """

    '''
    for pid in psutil.pids():
        p = psutil.Process(pid)
        print(pid, p.name())
        if 'cmd' == psutil.Process(pid).name():
            print(pid)
            break
    '''
    for proc in psutil.process_iter():
        try:
            if proc.name().lower() == pname.lower():
                return proc.pid  # return if found one
        except psutil.AccessDenied:
            pass
        except psutil.NoSuchProcess:
            pass
    return -1

def print_stock_info(stock_info):
    #['highest', 'lowest', 'last_min', 'cur', 'time_last_record', 'name']
    key_str = ['price', 'last_min', 'high', 'low']
    code = stock_info['code']
    cnt = time.strftime('[%H:%M:%S]', time.localtime()) + stock_info['name'] + '[%s]:' % str(code)
    for key in key_str:
        cnt += key + ':%.2f\t' % stock_info[key]
    print(cnt)

def pause_trade(day):
    today = datetime.date.today()
    if (today - day).days > 2:
        return True
    return False


# 标准日期格式 2016-01-01 str(datetime.date.today())
def get_day(day, delta):
    ymd = [int(i) for i in day.split('-')]
    day = datetime.date(ymd[0], ymd[1], ymd[2])
    day = day + datetime.timedelta(delta)

    return str(day)

def get_today():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))

def get_diff_days(day1, day2):
    ymd = [int(i) for i in day1.split('-')]
    date1 = datetime.date(ymd[0], ymd[1], ymd[2])
    ymd = [int(i) for i in day2.split('-')]
    date2 = datetime.date(ymd[0], ymd[1], ymd[2])

    return (date2 - date1).days

if __name__ == '__main__':
    #r = get_day('2015-12-31', 1)
    r = get_diff_days('2015-12-31','2016-01-10')
    print(r)
