#-*- coding: utf-8 -*-

import config.config as config
import acquisition.util as util

from acquisition.plugin.ht import ht_ma
from acquisition.plugin.dt import dt_ma

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
def second_wave2(quote, begin=config.SECOND_DAY, last_n_maN=config.SECOND_LAST_N_MA):
    if not hp_ma(quote, 30, 20, almost=1):
        return False

    ma_arr_all = util.gen_ma(quote)

    if not util.almost_equal(ma_arr_all[0]['ma'][-1], ma_arr_all[2]['ma'][-1]):
        return False

    if 100 * (ma_arr_all[0]['ma'][-1] - ma_arr_all[4]['ma'][-1]) / ma_arr_all[4]['ma'][-1] > 5:
        return True

    return False


