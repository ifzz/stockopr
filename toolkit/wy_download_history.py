#-*- encoding:utf-8 -*-
import sys
import pymysql.cursors
import urllib.request
import time
import os
import socket

sys.path.append(".")
sys.path.append("monitor")

#import stock.monitor.mysqlcli
import util.basic as basic


# timeout in seconds
timeout = 5
socket.setdefaulttimeout(timeout)

dataUrl='http://table.finance.yahoo.com/table.csv?a=0&b=1&c=2012&d=3&e=19&f=2012&s=600109.ss'
dataUrl='http://table.finance.yahoo.com/table.csv?s=600109.ss'
dataUrl='http://table.finance.yahoo.com/table.csv?s={}'
dataUrl='http://quotes.money.163.com/service/chddata.html?code={}&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP' # 0->sh, 1->sz
ex = 'ss'
#r,c=httplib2.request(dataUrl)
#print(r,c)
#exit(0)

def get_connection():
    connection = pymysql.connect(host='localhost',
            user='root', #'test',
            password='jkimjl106224', #'123456',
            db='test',
            #charset='utf8mb4',
            charset='utf8',
            #use_unicode=True,
            #init_command='SET NAMES UTF8',
            cursorclass=pymysql.cursors.DictCursor)
    return connection

stat_file = 'stat'
error_file = 'error'
error_file_bk = 'error_bk'

from_code = int('000001')
#if os.path.exists(stat_file):
#    with open(stat_file, 'r') as fp:
#        line = fp.readline()
#        from_code = line.strip()
#
#from_code = int(from_code)
#
#_stock_list = []
#
#for l in r:
#    _code_str = l['code']
#    _code = int(_code_str)
#    if _code <= from_code:
#        continue
#    _stock_list.append(l['code'])

# 设置代理
def set_proxy():
    pass
    #proxy_server = '192.126.123.132'
    #proxy_port = 9998
    #proxy_support = urllib.request.ProxyHandler({'sock5': '{}:{}'.format(proxy_server, proxy_port)})
    #opener = urllib.request.build_opener(proxy_support)
    #urllib.request.install_opener(opener)

#a = urllib.request.urlopen("http://g.cn").read()


#print(_stock_list)

def download_history_163(_code_str, LOG=True):
    _code_str = _code_str.strip()
    _code = int(_code_str)
    if LOG and _code < from_code:
        return

    _ex = '0' if _code >= 600000 else '1'
    _code_str_bk = _code_str
    _code_str = '{1}{0}'.format(_code_str, _ex)
    _dataUrl = dataUrl.format(_code_str)
    _csv = 'data/csv/{}.csv'.format(_code_str_bk)

    if os.path.exists(_csv):
        return

    # 只允成功，不许失败
    try_ = 5
    while try_ > 0:
        try:
            urllib.request.urlretrieve(_dataUrl, _csv)
            print('{0} ok'.format(_code_str))

            # 处理 error 时就不用记录了
            if LOG:
                with open(stat_file, 'w') as fp:
                    fp.write(_code_str_bk)

            time.sleep(0.2)
            break
        except Exception as e:
            try_ -= 1
            if try_ == 0:
                with open(error_file, 'a') as fp:
                    print('{1} {0}'.format(_dataUrl, e))
                    fp.write('{}\n'.format(_code_str_bk))
                break

            time.sleep(0.2)
            continue


def download_history(_code_str, LOG=True):
    _code = int(_code_str)
    if LOG and _code <= from_code:
        return

    _ex = 'ss' if _code >= 600000 else 'sz'
    _code_str_bk = _code_str
    _code_str = '{}.{}'.format(_code_str, _ex)
    _dataUrl = dataUrl.format(_code_str)
    _csv = '{}.csv'.format(_code_str)

    if os.path.exists(_csv):
        return

    # 只允成功，不许失败
    try_ = 5
    while try_ > 0:
        try:
            urllib.request.urlretrieve(_dataUrl, _csv)
            print('{0} ok'.format(_code_str))
            # 处理 error 时就不用记录了
            if LOG:
                with open(stat_file, 'w') as fp:
                    fp.write(_code_str_bk)

            time.sleep(0.5)
            break
        except Exception as e:
            try_ -= 1
            if try_ == 0:
                with open(error_file, 'a') as fp:
                    print('{1} {0}'.format(_dataUrl, e))
                    fp.write('{}\n'.format(_code_str_bk))
                break

            time.sleep(3)
            continue

def download_list_history(_stock_list, LOG=True):
    for _code_str in _stock_list:
        #download_history(_code_str, LOG)
        download_history_163(_code_str, LOG)

def get_stock_list_error():
    _stock_list_error = []
    try:
        with open(error_file, 'r') as fp:
            for code in fp:
                _stock_list_error.append(code.strip())
        os.rename(error_file, error_file_bk)
    except Exception as e:
        pass
        #print(e)
    return _stock_list_error

if __name__ == '__main__':
    if not os.path.exists('data/csv'):
        os.makedirs('data/csv')

    _stock_list = basic.get_all_stock_code()
    #_stock_list = ['002806', '300517', '300523', '300525', '601966', '603069']
    #_stock_list = ['002425']
    print(_stock_list)

    idx_max = 3
    idx = idx_max
    while True:
        #
        if os.path.exists(error_file_bk):
            with open(error_file_bk, 'r') as fp:
                if not fp.readline():
                    break

        print('+++++ {}'.format(idx_max - idx + 1))

        # 处理出错部分
        _stock_list_error = get_stock_list_error()
        download_list_history(_stock_list_error, False)
        # 下载
        download_list_history(_stock_list)
        idx -= 1
        if idx == 0:
            break

        #time.sleep(60)

exit(0)

#dataUrl = 'http://www.baidu.com'
cmd = 'curl -o xxx {0}'.format(dataUrl)
cmd = 'wget {0}'.format(dataUrl)
#cmd = 'curl -O {}'.format(dataUrl)
#cmd = 'curl -O %s'%dataUrl
print(cmd)
#cmd = 'ls'
#p = subprocess.Popen(cmd)
#p = subprocess.Popen('/bin/bash -c "{}"'.format(cmd))
p = subprocess.Popen(['/bin/bash', '-c', '{0}'.format(cmd)])
p.wait()

#urllib2.urlopen -> urllib.request.urlopen
stdout = urllib.request.urlopen(dataUrl)
with open('t.csv', 'w') as fp:
    fp.write(str(stdout))
