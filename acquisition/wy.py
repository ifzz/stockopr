#-*- encoding:utf-8 -*-

'''
from pandas.io.json import json_normalize
data = json.loads(elevations)
json_normalize(data['results'])

r = pd.read_json(json.dumps(quote))
'''

import datetime
import json
import urllib.request
import pandas as pd

import util.mysqlcli as mysqlcli

# 获取全部数据: page=0, count=0
#url = 'http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page={0}&query=STYPE%3AEQA&fields=NO%2CSYMBOL%2CNAME%2CPRICE%2CPERCENT%2CUPDOWN%2CFIVE_MINUTE%2COPEN%2CYESTCLOSE%2CHIGH%2CLOW%2CVOLUME%2CTURNOVER%2CHS%2CLB%2CWB%2CZF%2CPE%2CMCAP%2CTCAP%2CMFSUM%2CMFRATIO.MFRATIO2%2CMFRATIO.MFRATIO10%2CSNAME%2CCODE%2CANNOUNMT%2CUVSNEWS&sort=PERCENT&order=desc&count={1}&type=query'
url = 'http://quotes.money.163.com/hs/service/diyrank.php?host=http%3A%2F%2Fquotes.money.163.com%2Fhs%2Fservice%2Fdiyrank.php&page={0}&query=STYPE%3AEQA&sort=PERCENT&order=desc&count={1}&type=query&fields='

'''
{"page":0,"count":1,"order":"desc","total":3179,"pagecount":3179,"time":"2017-04-04
17:07:06","list":[{"CODE":"1300636","FIVE_MINUTE":0,"HIGH":20.84,"HS":0.00018005,"LB":1.0044630404463,"LOW":18.94,"MCAP":416800000,"MFRATIO":{"MFRATIO2":57996315.13,"MFRATIO10":250078505.36},"MFSUM":0.97,"NAME":"N\u540c\u548c","OPEN":18.94,"PE":21.484536082474,"PERCENT":0.440221,"PRICE":20.84,"SNAME":"\u540c\u548c\u836f\u4e1a","SYMBOL":"300636","TCAP":1667200000,"TURNOVER":75037.94,"UPDOWN":6.37,"VOLUME":3601,"WB":0,"YESTCLOSE":14.47,"ZF":0.13130615065653,"NO":1}]}"}]}
'''

#key_list = ['code', 'trade_date', 'close', 'high', 'low', 'open', 'yestclose', 'updown', 'percent', 'hs', 'volume', 'turnover', 'zf']

# notice: price close
key_list = [
'symbol',
'trade_date',
'price',
'high',
'low',
'open',
'yestclose',
'updown',
'percent',
'hs',
'volume',
'turnover',
'lb',
'wb',
'zf',
'five_minute'
]

def format_fields():
    _fields = ''
    for key in key_list:
        _fields += key.upper()
        _fields += '%2C'
    _fields = _fields[:-3]
    _url = url + _fields

    return _url

# 暂时不用, 先简化处理
def get_overview():
    _url = url.format(0, 0)
    r = urllib.request.urlopen(_url)
    data = stdout.read().decode('gbk')
    data = json.loads(data)

def _get_quote(page, count):
    _url = format_fields()
    _url = _url.format(page, count)
    r = urllib.request.urlopen(_url)
    data = r.read().decode('gbk')
    data = json.loads(data)

    quote = data['list']
    df = pd.read_json(json.dumps(quote), dtype=False)
    df.drop('NO', 1, inplace=True)
    df.rename(columns={'PRICE':'CLOSE', 'SYMBOL':'CODE'}, inplace=True)
    df['trade_date'] = str(datetime.date.today())

    return df

def get_quote():
    return _get_quote(0, 0)
