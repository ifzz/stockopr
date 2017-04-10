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

def zf(quote):
    # Series.any() Series.all()
    # 20天前, 还在整理
    nday = config.ZF_NDAY
    df_quote = quote[len(quote)-nday:]['zf'] # Series
    # df_quote.mean()
    if df_quote.min() > config.ZF_PERCENT_MIN and df_quote.mean() < config.ZF_PERCENT_AVG_MAX:
        return True

    return False
