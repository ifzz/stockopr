#-*- encoding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from util.macd import macd, sar, dmi, bbands, cci, rsi
from util.macd import adjust
import config.config as config
#import price

# 横盘, 60-80日均线, 5日macd 3值均约等于0
# 1 突破10日新高2%, macdhist > 0
# 2 macd金叉
# config.B/config.S/None
def gold_dead_macd(prices):
    df = macd(prices)
    macd_info = adjust(df, prices)
    yest = macd_info['macdhist'][-2]
    today = macd_info['macdhist'][-1]
    if abs(today) <= config.macd_threshold_0 or yest * today < 0:
        print('macd:\np:{0}\tc:{1}'.format(yest, today))
        if yest < 0:
            return config.B
        else:
            return config.S
    return ''

def gold_dead_sar(prices):
    df = sar(prices)
    macd_info = adjust(df, prices)
    yest = macd_info['sar'][-2] - macd_info['close'][-2]
    today = macd_info['sar'][-1] - macd_info['close'][-1]
    if abs(today) <= config.macd_threshold_0 or yest * today < 0:
        print('sar:\np:{0}\tc:{1}'.format(yest, today))
        if yest < 0:
            return config.S
        else:
            return config.B
    return ''

def gold_dead_dmi(prices):
    macd_info = dmi(prices)
    if macd_info['adx'][-1] <= 20:
        return

    yest = macd_info['pdi'][-2] - macd_info['mdi'][-2]
    today = macd_info['pdi'][-1] - macd_info['mdi'][-1]
    if abs(today) <= config.macd_threshold_0 or yest * today < 0:
        print('dmi:\np:{0}\tc:{1}'.format(yest, today))
        if yest < 0:
            return config.B
        else:
            return config.S
    return ''

def gold_dead_bbands(prices):
    macd_info = dmi(prices)
    if macd_info['adx'][-1] <= 20:
        return

    yest = macd_info['pdi'][-2] - macd_info['mdi'][-2]
    today = macd_info['pdi'][-1] - macd_info['mdi'][-1]
    if abs(today) <= config.macd_threshold_0 or yest * today < 0:
        print('dmi:\np:{0}\tc:{1}'.format(yest, today))
        if yest < 0:
            return config.B
        else:
            return config.S
    return ''

def gold_dead_cci(prices):
    macd_info = cci(prices)
    yest = macd_info['cci'][-2]
    today = macd_info['cci'][-1]
    # TODO
    # W
    if today < -100:
        return config.B
    # M
    elif today > 100 and today > yest:
        return config.S
    return ''

def gold_dead_rsi(prices):
    macd_info = macd(prices)
    yest = macd_info['rsi_12'][-2]
    today = macd_info['rsi_24'][-1]
    # TODO
    # rsi 14, 40-90
    # rsi 14, 10-60
    if abs(today) <= config.macd_threshold_0 or yest * today < 0:
        if yest < 0:
            return config.B
        else:
            return config.S
    return ''

def gold_dead(prices):
    signal_macd = gold_dead_macd(prices)
    signal_dmi = gold_dead_dmi(prices)
    signal_sar = gold_dead_sar(prices)
    signal = '{0}{1}{2}'.format(signal_macd, signal_dmi, signal_sar)
    count_b = signal.count(config.B)
    count_s = signal.count(config.S)
    if count_b + count_s == 0:
        return ''

    print(signal)
    if count_s == 0 or 100*count_b/(count_b+count_s) > 50:
        return config.B
    if count_b == 0 or 100*count_s/(count_b+count_s) > 50:
        return config.S


def test_macd(prices):
    r = 0
    e = 0
    macd3 = macd(prices)
    skip = 1
    for i,_ in enumerate(macd3):
        if i < skip:
            continue

        if macd3[i]['macdhist'] > 0 and macd3[i - 1]['macdhist'] <= 0:
            print('up', macd3[i]['trading_date'])
            n = len(macd3) - i
            for j in range(1, n):
                if macd3[i + j]['macdhist'] < 0: # and macd3[i-1]['sar'] < macd3[i-1]['close']:
                    diff = round(prices[i + j - 1]['close'] - prices[i]['close'], 2)
                    print(macd3[i + j - 1]['trading_date'], diff, round(100*(diff)/prices[i]['close'], 2))
                    if diff < 0:
                        e += 1
                        print('oh, no')
                    else:
                        r += 1

                    skip = i + j
                    break
                #print('{0}\t{1}'.format(macd3[i + j - 1]['macdhist'], prices[i + j - 1]['close']))
                print('{0}\t{1}'.format(macd3[i + j]['macdhist'], prices[i + j]['close']))

            else:
                j = n - 1
                diff = round(prices[i + j]['close'] - prices[i]['close'], 2)
                print(macd3[i + j]['trading_date'], diff, round(100*(diff)/prices[i]['close'], 2))
                if diff < 0:
                    e += 1
                    print('oh, no')
                else:
                    r += 1

                skip = i + n
            print('+'*10)
        elif _['macdhist'] < 0 and macd3[i - 1]['macdhist'] >= 0:
            print('down', macd3[i]['trading_date'])
            n = len(macd3) - i
            for j in range(n):
                if macd3[i + j]['macdhist'] > 0: # and macd3[i-1]['sar'] < macd3[i-1]['close']:
                    diff = round(prices[i + j - 1]['close'] - prices[i]['close'], 2)
                    print(macd3[i + j - 1]['trading_date'], diff, round(100*(diff)/prices[i]['close'], 2))
                    if diff > 0:
                        e += 1
                        print('oh, no')
                    else:
                        r += 1

                    skip = i + j
                    break
                #print('{0}\t{1}'.format(macd3[i + j - 1]['macdhist'], prices[i + j - 1]['close']))
                print('{0}\t{1}'.format(macd3[i + j]['macdhist'], prices[i + j]['close']))
            else:
                j = n - 1
                diff = round(prices[i + j]['close'] - prices[i]['close'], 2)
                print(macd3[i + j]['trading_date'], diff, round(100*(diff)/prices[i]['close'], 2))
                if diff > 0:
                    e += 1
                    print('oh, no')
                else:
                    r += 1

                skip = i + n
            print('+'*10)
    print(r, e, round(100*r/(r+e), 2))

def test_sar(prices):
    r = 0
    e = 0
    sar2 = sar(prices)
    sar2 = sar2[-60:]
    _len = len(sar2.index)
    #sar2.shape #(250, 2)
    #sar2['close'].count()
    #for _ in sar2:
    #    print(_)

    mask = (sar2['close'] > sar2['sar'])
    sar2['trend'] = mask
    #mask = (((sar2['r'] == True) & (sar2['r'].shift(1) == False)) | ((sar2['r'] == False) & (sar2['r'].shift(1) == True)))
    mask = (((sar2['close'] > sar2['sar']) & (sar2['close'].shift(1) < sar2['sar'].shift(1))) | ((sar2['close'] < sar2['sar']) & (sar2['close'].shift(1) > sar2['sar'].shift(1))))
    sar2['signal'] = mask

    #for i in range(_len):
    #    print(sar2['close'][i])
    #exit(0)
    #duration = sar2['signal'][sar2['signal'] == True].index
    duration = sar2[sar2['signal'] == True].index
    #last_index = sar2.last_valid_index()
    #if duration[-1] != last_index:
    #    print(type(duration))
    #    print(duration[-1])
    #    #duration.insert(last_index, None)
    #print(duration)

    #print((sar2['signal'] == True).argmax()) # 返回第一个
    #list(sar2['signal']).index(True) # 不靠谱, 就是 python 的 list
    #print(sar2.loc[duration[0]:duration[1]])
    #print(sar2[duration[0]:duration[1]])
    #print(sar2[duration[0]:duration[0]])

    def check(b, e):
        r = True
        _b = b['close'].reset_index()
        _e = e['close'].reset_index()
        if b['trend'][0] == True:
            print('up')
            diff = _e - _b
        else:
            print('down')
            diff = _b - _e
        if diff['close'][0] < 0:
            r = False
        print(100*diff['close'][0]/_b['close'][0])

        return r

    f = 0
    a = len(duration)
    b = sar2.iloc[0:1,]
    for i in range(len(duration)):
        e = sar2.loc[duration[i]:duration[i]]

        if not check(b, e):
            f += 1

        b = e
    if b.index != sar2.iloc[-1:].index:
        a += 1
        e = sar2.iloc[-1:]
        if not check(b, e):
            f += 1

    print('\n+++ {0}% +++'.format(100*f/a))
    import pandas as pd
    #for _ in sar2['r'].__iter__():
    #    print(_)
    #for i, _ in sar2['r'].iteritems():
    #    print(i, _)
    #exit(0)

if __name__ == '__main__':
    code = "600528"
    code = "600839"
    code = "600674"
    #code = "600519"
    import price
    #p = price.get_price_info_list_db(code, 250)
    p = price.get_price_info_df_db(code, 250)
    func_list = ['ma', 'macd', 'sar', 'dmi', 'bbands', 'kdj', 'cci', 'rsi', 'bias', 'atr']
    func = 'ma'
    r = eval(func)(p)
    r = r[-60:]
    print(r)
    if func.find('test') >= 0:
        exit(0)
    if func.find('gold') >= 0:
        exit(0)
    #test_macd(p)
    #print(r.describe())
    #test_sar(p)
    #exit(0)

    #plt.figure(figsize=(8,6), dpi=80)
    plt.figure()

    r.plot()
    plt.savefig('png/{0}'.format(func))
