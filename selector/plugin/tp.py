#-*- coding: utf-8 -*-

from util.macd import ma
import config.config as config
import selector.util as util
from selector.plugin._dt import dt_ma
from selector.plugin.hp import hp_ma

def tp_ma(quote, maN=config.TP_MA_N, almost=config.ALMOST_EQUAL, range=config.TP_RANGE):
    ma20 = ma(quote, maN)
    if not util.almost_equal(quote.close[-1], ma20.ma[-1], almost):
        return False

    ma_arr = util.gen_ma(quote)
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


