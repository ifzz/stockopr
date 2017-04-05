#-*- coding: utf-8 -*-

from util.macd import ma

import config.config as config
import acquisition.util as util

# 回调到ma30支撑点
def ht_ma(quote, maN=config.HT_MA_N, almost=config.ALMOST_EQUAL, range=config.HT_RANGE):
    ma_arr = util.gen_ma(quote)
    r = 100*(ma_arr[0]['ma'][-1] - ma_arr[-1]['ma'][-1])/ma_arr[-1]['ma'][-1]
    if r < range:
        return False

    #print(quote['code'][-1])
    #print(r)
    ma30 = ma(quote, maN)
    #if not almost_equal(quote.close[-1], ma30.ma[-1], almost):
    if util.almost_equal(quote.close[-1], ma30.ma[-1], almost):
        return True

    if util.almost_equal(quote.low[-1], ma30.ma[-1], almost):
        return True

    if quote.low[-1] < ma30.ma[-1]:
        return True

    return False


