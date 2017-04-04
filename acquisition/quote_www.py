#-*- encoding: utf-8 -*-

import urllib.request
import re
import time
import datetime
import config

import util.mysqlcli as mysqlcli

import pandas as pd
import json

def get_price_urllib(stock_code):
    exchange = "0" if (int(stock_code) // 100000 == 6) else "1"
    _stock_code = '{1}{0}'.format(stock_code, exchange)
    if stock_code == '999999':
        _stock_code = '0000001'
    r = urllib.request.urlopen('http://api.money.126.net/data/feed/{0},money.api'.format(_stock_code)).read().decode()
    b = r.find(':{') + 1
    e = r.find(' }')
    data = json.loads(r[b:e])
    percent = float(data['percent']) * 100
    percent = round(percent, 2)
    #print(data['name'], percent, data['time'])
    #print(stock_code, percent, data['time'])
    print('{0}\t{1}\t{2}\t{3}'.format(data['symbol'], percent, data['price'], data['time']))
    #key_list = ['code', 'trade_date', 'open', 'high', 'low', 'close', 'volume', 'turnover'] #mysql
    key_list = ['trade_date', 'open', 'high', 'low', 'close', 'volume', 'turnover']
    val_list = [stock_code]
    for key in key_list:
        if key == 'trade_date':
            tm = time.strptime(data['update'], '%Y/%m/%d %H:%M:%S')
            val = time.strftime('%F', tm)
            if tm.tm_hour < 15:
                return None
        elif key == 'close':
            val = data['price']
        else:
            val = data[key]
        val_list.append(val)

    return tuple(val_list)

#国内股票数据：指数
def getChinaStockIndexInfo(stockCode, period):
    try:
        exchange = "sz" if (int(stockCode) // 100000 == 3) else "sh"
        #http://hq.sinajs.cn/list=s_sh000001
        dataUrl = "http://hq.sinajs.cn/list=s_" + exchange + stockCode
        stdout = urllib.request.urlopen(dataUrl)
        stdoutInfo = stdout.read().decode('gbk')
        #print(stdoutInfo) #var hq_str_s_sh000001="上证指数,4121.715,87.405,2.17,5898142,78166734";

        tempData = re.search('''(")(.+)(")''', stdoutInfo).group(2)
        stockInfo = tempData.split(",")
        #stockCode = stockCode,
        stockName   = stockInfo[0]
        stockEnd    = stockInfo[1]  #当前价，15点后为收盘价
        stockZD     = stockInfo[2]  #涨跌
        stockLastEnd= str(float(stockEnd) - float(stockZD)) #开盘价
        stockFD     = stockInfo[3]  #幅度
        stockZS     = stockInfo[4]  #总手
        stockZS_W   = str(int(stockZS) / 100)
        stockJE     = stockInfo[5]  #金额
        stockJE_Y   = str(int(stockJE) / 10000)
        content = "#" + stockName + "#" + "(" + str(stockCode) + ")" + " 收盘：" \
          + stockEnd + "，涨跌：" + stockZD + "，幅度：" + stockFD + "%" \
          + "，总手：" + stockZS_W + "万" + "，金额：" + stockJE_Y + "亿" + "  "

        imgPath = "http://image.sinajs.cn/newchart/" + period + "/n/" + exchange + str(stockCode) + ".gif"
        twitter = {'message': content, 'image': imgPath}

    except Exception as e:
        print(">>>>>> Exception: " + str(e))
    else:
        return twitter
    finally:
        None

def getChinaStockIndividualPriceInfoTx(stockCode):
    try:
        exchange = "sh" if (int(stockCode) // 100000 == 6) else "sz"
        url = 'http://qt.gtimg.cn/q={}{}'.format(exchange, stockCode)
        r = urllib.request.urlopen(url)
        if not r:
            return None

        #stdoutInfo = r.read().decode('gb2312')
        # utf-8 default
        # UnicodeDecodeError: 'utf-8' codec can't decode byte 0xce in position 15: invalid continuation byte
        stdoutInfo = r.read().decode('gbk')
        r = re.search('.*="(.*)";', stdoutInfo)
        if r:
            stockInfo = r.group(1).split('~')
        else:
            return None

        stockName   = stockInfo[1]  #名称
        stockStart  = stockInfo[5]  #开盘
        stockLastEnd= stockInfo[4]  #昨收盘
        stockCur    = stockInfo[3]  #当前
        stockMax    = stockInfo[41]  #最高
        stockMin    = stockInfo[42]  #最低
        stockUp     = round(float(stockCur) - float(stockLastEnd), 2)
        stockVol = stockInfo[6]
        date = stockInfo[30]
        stockDate = '{}-{}-{}'.format(date[:4],date[4:6],date[6:8])

        return {"name":stockName, 'trade_date':stockDate, 'code':stockCode, 'open':stockStart, 'high':stockMax, 'low':stockMin, 'close':stockCur, 'volume':stockVol, 'adj_close':0}
    except Exception as e:
        print(e, stockCode)
        return None

#国内股票数据：个股
def getChinaStockIndividualPriceInfoWy(stockCode):
    try:
        exchange = "0" if (int(stockCode) // 100000 == 6) else "1"
        stock_code_wy = '{1}{0}'.format(stockCode, exchange)
        dataUrl = "http://api.money.126.net/data/feed/{0},money.api".format(stock_code_wy)
        #stdout = urllib.request.urlopen(dataUrl, data = None, timeout=3)
        stdout = urllib.request.urlopen(dataUrl)
        stdoutInfo = stdout.read().decode('gbk')
        # _ntes_quote_callback({"0603077":{"code": "0603077", "percent": 0.100583, "share": "1", "high": 7.55, "askvol3": 0, "askvol2": 0, "askvol5": 0, "askvol4": 0, "price": 7.55, "open": 6.92, "bid5": 7.51, "bid4": 7.52, "bid3": 7.53, "bid2": 7.54, "bid1": 7.55, "low": 6.82, "updown": 0.69, "type": "SH", "symbol": "603077", "status": 0, "ask4": 0.0, "bidvol3": 42800, "bidvol2": 38300, "bidvol1": 21922303, "update": "2015/11/20 15:59:55", "bidvol5": 68300, "bidvol4": 26500, "yestclose": 6.86,
        # "askvol1": 0, "ask5": 0.0, "volume": 86558989, "ask1": 0.0, "name": "\u548c\u90a6\u751f\u7269", "ask3": 0.0, "ask2": 0.0, "arrow": "\u2191", "time": "2015/11/20 15:59:51", "turnover": 632902972} });
        b = stdoutInfo.find('(')
        e = stdoutInfo.find(')')
        ret = stdoutInfo[b+1:e]
        d = json.loads(ret)
        stockInfo = d[stock_code_wy]

        #stockCode = stockCode,
        stockName   = stockInfo['name']  #名称
        stockStart  = stockInfo['open']  #开盘
        stockLastEnd= stockInfo['yestclose']  #昨收盘
        stockCur    = stockInfo['price']  #当前
        stockMax    = stockInfo['high']  #最高
        stockMin    = stockInfo['low']  #最低
        stockUp     = stockInfo['updown']
        stockRange  = stockInfo['percent']

        stockVol = stockInfo['volume']
        stockTurnover = stockInfo['turnover']
        stockDate = stockInfo['time'] # 2015/11/20 15:59:51 -> 2015-11-20
        return {"name":stockName, 'trade_date':stockDate, 'code':stockCode, 'open':stockStart, 'high':stockMax, 'low':stockMin, 'close':stockCur, 'yestclose':stockLastEnd, 'volume':stockVol, 'turnover':stockTurnover, 'adj_close':0}

    except Exception as e:
        if str(e).find('delete') >= 0:
            raise e
        print(">>>>>> Exception: " + str(e), stockCode)
        #engine.say('网络错误')
        #engine.runAndWait()
        return None
    else:
        return twitter
    finally:
        None

#国内股票数据：个股
def getChinaStockIndividualPriceInfo(stockCode):
    try:
        exchange = "sh" if (int(stockCode) // 100000 == 6) else "sz"
        dataUrl = "http://hq.sinajs.cn/list=" + exchange + stockCode
        #stdout = urllib.request.urlopen(dataUrl, data = None, timeout=3)
        stdout = urllib.request.urlopen(dataUrl)
        stdoutInfo = stdout.read().decode('gbk')
        #print(stdoutInfo) #var hq_str_sz300168="万达信息,107.870,112.000,108.500,112.000,104.990,108.500,108.530,12045414,1296802069.350,9165,108.500,500,108.490,2000,108.480,300,108.400,100,108.380,200,108.530,400,108.600,600,108.610,200,108.630,400,108.650,2015-04-13,15:05:53,00";

        tempData = re.search('''(")(.+)(")''', stdoutInfo).group(2)
        stockInfo = tempData.split(",")
        #stockCode = stockCode,
        stockName   = stockInfo[0]  #名称
        stockStart  = stockInfo[1]  #开盘
        stockLastEnd= stockInfo[2]  #昨收盘
        stockCur    = stockInfo[3]  #当前
        stockMax    = stockInfo[4]  #最高
        stockMin    = stockInfo[5]  #最低
        stockUp     = round(float(stockCur) - float(stockLastEnd), 2)
        stockRange  = round(100 * float(stockUp) / float(stockLastEnd), 2)


        #twitter = {'message': content}
        twitter = {"name":stockName, "code":stockCode, "yestclose":stockLastEnd, "open":stockStart, "price":stockCur, "high":stockMax, "low":stockMin, "updown":stockUp, "percent":stockRange}

    except Exception as e:
        print(">>>>>> Exception: " + str(e))
        #engine.say('网络错误')
        #engine.runAndWait()
        return None
    else:
        return twitter
    finally:
        None


if __name__ == '__main__':
    pass
    #r = get_price_info_db('600839', '2015/12/31')
    #r = get_price_info_df_db('600839', 1)
    #r = get_price_info_df_db('600839', datetime.date(2016, 11, 1), 1, 'D')
    r = get_price_info_df_db_day('600839', '', 1)
    print(r)
