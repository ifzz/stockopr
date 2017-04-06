#-*- coding: utf-8 -*-

import config.config as config
import selector.util as util

# begin天的maN成多头排列
# 1, 4, 今天的ma10-ma60成多头排列
# 多头排列, ma20, ma40, ma60, 在之前第n天成多头排列
# 默认多头排列, ma5, ma10, ma20, ma40, ma60, 在今天成多头排列
# r: 取maN的后n个
def dt_ma(quote, begin=config.DT_DAY, last_n_maN=config.DT_LAST_N_MA):
    ma_arr_all = util.gen_ma(quote)
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
def dt_ma2(quote, p=config.DT_MIN_UP_P):
    ma_arr = util.gen_ma(quote)
    if 100 * (ma_arr[0]['ma'][-1] - ma_arr[4]['ma'][-1]) / ma_arr[4]['ma'][-1] > p:
        return True
    return False

def dt_boll(quote, b=config.DT_BOLL_DAY, d=config.DT_BOLL_DAY_AGO):
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
def dt_sar(quote, b=config.DT_SAR_DAY):
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
