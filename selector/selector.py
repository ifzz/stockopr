#-*- coding: utf-8 -*-
'''

1 横盘时间

'''
import sys
import time

import acquisition.basic as basic
import acquisition.quote_db as price

import selector.selected as selected

import util.util as util

from util.macd import ma
from util.macd import bbands
from util.macd import dmi
from util.macd import macd
from util.macd import sar

import numpy as np
import pandas

#import future

T = 'W'
T = 'D'
D_MIN = 250
W_MIN = 52
MIN = D_MIN if T == 'D' else W_MIN

DZ_MIN = 120 if T == 'D' else 25
DD_MIN = 120 if T == 'D' else 25

# 1.1^5 = 1.61
DZ_PERCENT_LIMIT = 11 if T == 'D' else 61
# 0.9^5 = 59.04
DD_PERCENT_LIMIT = 11 if T == 'D' else 41

BOLL_BACK = 20 if T == 'D' else 4
BOLL_DURATION = 60 if T == 'D' else 12

def almost_equal(m, n, almost=1):
    l = m
    if m > n:
        l = n
    if abs(m - n) * 100 / l < almost:
        return True
    return False

def gen_ma(quote, n=5, l=[5, 10, 20, 30, 60]):
    r = []
    for i in range(n):
        r.append(ma(quote, l[i]))

    return r

# 多头排列, ma20, ma40, ma60, 在之前第n天成多头排列
# 默认多头排列, ma5, ma10, ma20, ma40, ma60, 在今天成多头排列
# r: 取maN的后n个
def dt_ma(quote, begin=1, last_n_maN=4):
    ma_arr_all = gen_ma(quote)
    len_ma_arr = len(ma_arr_all)
    ma_arr = ma_arr_all[len_ma_arr-last_n_maN:]

    # n天, 多头格局
    for t in range(1, begin+1):
        l = [i['ma'][-1*t] for i in ma_arr]
        s = sorted(l, reverse=True)
        if s != l:
            return False
        #if l[-1] > l[-2]:
        #    return False

    ## 短期回调, 不可能出现ma5 < ma20
    #if ma_arr_all[0]['ma'][-1] <= ma_arr[0]['ma'][-1]:
    #    return False

    #len_ma_arr = len(ma_arr)
    #for i in range(len_ma_arr):
    #    b = ma_arr[i]['ma'] > ma_arr[i]['ma'].shift(1)
    #    b = b[-5:]
    #    if not b.all():
    #        return False

    return True

# ma5 - ma60 > 5%
def dt_ma2(quote, b=1):
    ma_arr = gen_ma(quote)
    if 100 * (ma_arr[0]['ma'][-1] - ma_arr[4]['ma'][-1]) / ma_arr[4]['ma'][-1] > 5:
        return True
    return False

def dt_boll(quote, b=10, d=60):
    r = bbands(quote)
    l = r['middleband'][-(b+int(d/2))]
    m = r['middleband'][-1]
    if m <= l:
        return False

    return True


def dt_macd(quote):
    r = macd(quote)
    if r['macdhist'][-1] < 0:
        return False
    return True

# +di > -di and adx > 25
# Wilder suggests that a strong trend is present when ADX is above 25 and no trend is present when below 20.
# There appears to be a gray zone between 20 and 25.
def dt_dmi(quote):
    r = dmi(quote)
    if r['pdi'][-1] < r['mdi'][-1]:
        return False
    if r['adx'][-1] < 25:
        return False
    return True

# 5天前的sar
def dt_sar(quote, b=5):
    r = sar(quote)
    b *= -1
    if r['close'][b] < r['sar'][b]:
        return False
    return True

def dt(quote):
    if not dt_ma(quote):
        return False
    if not dt_dmi(quote):
        return False
    if not dt_macd(quote):
        return False
    if not dt_sar(quote):
        return False

    return True

# boll 曲线中线也许更好一些
# r 表示取前n个ma
def hp_ma(quote, begin=1, duration=-1, first_n_maN=5, almost=1):
    if duration == -1:
        duration = begin
    ma_arr = gen_ma(quote)
    for j in range(int(begin-duration), begin):
        i = -1 - j
        l = min([ma_arr[k]['ma'][i] for k in range(first_n_maN)])
        m = max([ma_arr[k]['ma'][i] for k in range(first_n_maN)])
        if almost_equal(l, m, almost):
            #print('{0}\t{1}\t{2}'.format(l, m, (m-l)*100/l))
            return True
    return False

def hp_boll(quote, b=BOLL_BACK, d=BOLL_DURATION):
    r = bbands(quote)

    #l = min(r['middleband'][(b+d)*-1+1:(b+int(d/2))*-1+1])
    #m = max(r['middleband'][(b+d)*-1+1:(b+int(d/2))*-1+1])
    #if not almost_equal(l, m, 3):
    #    return False
    #l = min(r['middleband'][(b+int(d/2))*-1+1:b*-1+1])
    #m = max(r['middleband'][(b+int(d/2))*-1+1:b*-1+1])
    #if not almost_equal(l, m, 3):
    #    return False
    for i in range(5, b):
        l = min(r['middleband'][(i+d)*-1+1:i*-1+1])
        m = max(r['middleband'][(i+d)*-1+1:i*-1+1])
        if almost_equal(l, m, 5):
            return True
    return False

# 横盘也很多表现形式
def hp(quote):
    if not hp_ma(quote, first_n_maN=4, almost=1):
        return False

    return True

def hp_p(quote):
    if not hp(quote):
        return False
    if not hp_boll(quote):
        return False

    return True

def hp_pp(quote):
    if not hp_ma(quote, almost=2):
        return False

    return True

def hp_ppp(quote):
    if not hp_pp(quote):
        return False

    if not hp_boll(quote):
        return False

    return True

    '''
    day_list = [250, 120, 80, 60, 40, 30, 20, 10, 5]
    day_list = [80, 60, 40, 30, 20, 10, 5] #5, 横盘中, 突破由监控程序处理
    day_list = [60, 40, 30, 20, 10, 5] #5, 横盘中, 突破由监控程序处理
    day_list = [40, 30, 20, 10, 5] #5, 横盘中, 突破由监控程序处理
    day_list = [30, 20, 10, 5] #5, 横盘中, 突破由监控程序处理
    val_list = []
    for day in day_list:
        val_list.append(price.get_price_stat_db(code, 'p', day, 'avg'))
    val_max = max(val_list)
    val_min = min(val_list)
    diff = abs(val_max - val_min) * 100 / val_min
    # 长期横盘
    if diff < 50:
        # 加入监控列表
        print(code)
        #basic.add_selected(code)
    '''

def tp_ma(quote, maN=20, almost=1, range=5):
    ma20 = ma(quote, maN)
    if not almost_equal(quote.close[-1], ma20.ma[-1], almost):
        return False

    ma_arr = gen_ma(quote)
    if range < 100*(ma_arr[0]['ma'][-1] - ma_arr[-1]['ma'][-1])/ma_arr[-1]['ma'][-1] < range+1:
        return True

    return False

def tp(quote):
    # 20天前, 还在整理
    if not hp_ma(quote, 30, 10, almost=1):
        return False

    #if not hp_boll(quote):
    #    return False

    #if not hp_ma(quote, r=2):
    #    return False

    # ma30, ma60 向上
    if not dt_ma(quote, last_n_maN=2):
        return False

    if not tp_ma(quote, almost=1):
        return False

    return True

# 回调到ma30支撑点
def ht_ma(quote, maN=10, almost=1, range=10):
    ma_arr = gen_ma(quote)
    r = 100*(ma_arr[0]['ma'][-1] - ma_arr[-1]['ma'][-1])/ma_arr[-1]['ma'][-1]
    if r < range:
        return False

    #print(quote['code'][-1])
    #print(r)
    ma30 = ma(quote, maN)
    #if not almost_equal(quote.close[-1], ma30.ma[-1], almost):
    if almost_equal(quote.close[-1], ma30.ma[-1], almost):
        return True

    if almost_equal(quote.low[-1], ma30.ma[-1], almost):
        return True

    if quote.low[-1] < ma30.ma[-1]:
        return True

    return False

def second_wave(quote):
    # 20天前, 还在整理
    if not hp_ma(quote, 30, 30, almost=1):
        return False

    #if not hp_boll(quote):
    #    return False

    #if not hp_ma(quote, r=2):
    #    return False

    # ma30, ma60 向上
    if not dt_ma(quote, last_n_maN=2):
        return False

    #print(quote['code'][-1])

    if not ht_ma(quote, almost=2):
        return False

    return True

# ma5 == ma20
# ma5 - ma60 > 5%
def second_wave2(quote, begin=1, last_n_maN=4):
    if not hp_ma(quote, 30, 20, almost=1):
        return False

    ma_arr_all = gen_ma(quote)

    if not almost_equal(ma_arr_all[0]['ma'][-1], ma_arr_all[2]['ma'][-1]):
        return False

    if 100 * (ma_arr_all[0]['ma'][-1] - ma_arr_all[4]['ma'][-1]) / ma_arr_all[4]['ma'][-1] > 5:
        return True

    return False


# n天涨幅
def z(quote, percent_exp=15, nday=5):
    quote = quote[-1*nday:]
    #quote = price.get_price_info_df_db(code, nday)
    if len(quote) < nday:
        return False

    quote_close_yest = quote['close'].shift(1)
    percent = 100*(quote['close'] - quote_close_yest)/quote_close_yest
    percent = percent[pandas.notnull(percent)]
    if max(percent) > DZ_PERCENT_LIMIT:
        return False

    quote_close_min = min(quote['close'])
    quote_close_max = max(quote['close'])
    percent = 100 * (quote['close'][-1] - quote_close_min) / quote_close_min
    #percent = 100 * (quote_close_max - quote_close_min) / quote_close_min
    #max_percent = 1.1**nday - 1
    #if max_percent < percent:
    #    continue

    if percent > percent_exp:
        if util.pause_trade(quote.index.values[-1]):
            #print('{0}\t{1}\t{2} %(停牌)'.format(code, name, round(percent, 2)))
            return False
    else:
        return False
    print('%.2f%% %s' % (percent, '-'*50))

    return True

def dz(quote):
    return z(quote, 100, DZ_MIN)

# n天跌幅
# 10天跌15%, ma60向上
def d(quote, percent_exp=15, nday=5):
    quote = quote[-1*nday:]
    if len(quote) < nday:
        return False

    percent = 100*(quote['close'] - quote['close'].shift(1))/quote['close'].shift(1)
    #percent = percent[np.isfinite(percent)]
    percent = percent[pandas.notnull(percent)]
    #df.dropna()
    #df.dropna(how='all')

    if min(percent) < -1*DD_PERCENT_LIMIT:
        return False

    percent = 100 * (quote['close'][-1] - max(quote['close'])) / max(quote['close'])
    #max_percent = 1 - 0.9**nday
    #if max_percent < percent:
    #    continue
    if percent*-1 > percent_exp:
        from datetime import datetime
        if T == 'W':
            #>>> import numpy as np
            #>>> import pandas as pd
            #>>> pd.Timestamp(np.datetime64('2012-06-18T02:00:05.453000000-0400')).to_pydatetime()

            #datetime.datetime.utcfromtimestamp(x.tolist()/1e9)
            #datetime.datetime.utcfromtimestamp(x.astype('O')/1e9)
            #datetime.datetime.fromtimestamp(x.astype('O')/1e9)
            trade_date = quote.index.values[-1].astype('M8[D]').astype('O') #'M8[ms]'
        else:
            trade_date = quote.index.values[-1]
        if util.pause_trade(trade_date):
            #print('{0}\t{1}\t{2} %(停牌)'.format(code, name, round(percent, 2)))
            return False
    else:
        return False

    #print('{}%'.format(percent))
    #print('%.2f%% %s %s' % (percent, '-'*50, quote.code[-1]))
    print('%.2f%% %s' % (percent, '-'*50))

    return True

def dd(quote):
    return d(quote, 50, DD_MIN)

def filter_quote(quote):
    if len(quote) < MIN:
        return True
    return False

def filer_code(code):
    if basic.sum_trade_date(code) < MIN:
        return True
    return False

def test(quote):
    return
    r = gen_ma(quote)
    r_ = r[0].shift(1)
    print(r[0].ma[-3:], r_.ma[-3:])
    b = r[0].ma < r_.ma
    print(b.all())
    exit(0)
    r = dt_ma(quote, last_n_maN=5)
    exit(0)
    ht_ma(quote)
    exit(0)

def verify(code, dt=True):
    pass

def print_time(t):
    if int(cost/5) == 0:
        print(cost)

def print_line(a):
    if a % 100 == 0:
        n = int(a/100)
        print('{0}'.format('-'*n))

# NameError: name 'hp' is not defined, 不能放到文件最前面
# 横盘 第二波 突破 涨 跌 大涨 大跌
selector = {'hp':hp, 'hp_p':hp_p, 'hp_pp':hp_pp, 'hp_ppp':hp_ppp, '2nd':second_wave, '2nd2':second_wave2, 'tp':tp, 'z':z, 'dz':dz, 'd':d, 'dd':dd, 'test':test} #'dt':dt,

def select(cls='hp'):
    t1 = time.time()
    code_list = basic.get_all_stock_code()
    #code_list = future.get_future_contract_list()
    #print(code_list)
    #code_list = ['600886']
    a = len(code_list)
    print('+++ {0} {1} +++\n'.format(a, cls))

    pre_cost = 0
    cost = 0

    s = 0
    for code in code_list:
        a -= 1
        #print_line(a)
        cost = int(time.time()-t1)
        if cost != pre_cost:
            pre_cost = cost
            if cost % 5 == 0:
                print('{0}s\t{1}'.format(cost, a))

        p = price.get_price_info_df_db(code, 500, '', T)
        if filter_quote(p):
            continue

        rc = selector.get(cls)(p)
        if rc:
            s += 1
            print('{2}{0} {1}'.format(code, basic.get_stock_name(code), ' '*50))
            #print('{2}{0} {1}'.format(code, basic.get_future_name(code), ' '*50))
            # insert into selected
            selected.add_selected(code)

    t2 = time.time()
    print('\n+++ {0} +++\n+++ {1} +++'.format(s, int(t2 - t1)))
    print('\n计划你的交易 交易你的计划\n')

select('2nd2')

if __name__ == '__main__':
    #select('hp')
    #select('hp_p')
    #select('hp_pp')
    #select('tp')
    #select('2nd')
    select('2nd2')
    #select('z')
    #select('d')
    #select('dd')
    #select('z')
    #select('dz')
