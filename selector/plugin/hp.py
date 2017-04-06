#-*- coding: utf-8 -*-

import config.config as config
import selector.util as util

from util.macd import bbands

# boll 曲线中线也许更好一些
# r 表示取前n个ma
def hp_ma(quote, begin=config.HP_DAY, duration=config.HP_DURATION, first_n_maN=config.HP_FIRST_N_MA, almost=config.ALMOST_EQUAL):
    if duration == -1:
        duration = begin
    ma_arr = util.gen_ma(quote)
    for j in range(int(begin-duration), begin):
        i = -1 - j
        l = min([ma_arr[k]['ma'][i] for k in range(first_n_maN)])
        m = max([ma_arr[k]['ma'][i] for k in range(first_n_maN)])
        if util.almost_equal(l, m, almost):
            #print('{0}\t{1}\t{2}'.format(l, m, (m-l)*100/l))
            return True
    return False

def hp_boll(quote, b=config.HP_BOLL_BACK, d=config.HP_BOLL_DURATION):
    r = bbands(quote)

    #l = min(r['middleband'][(b+d)*-1+1:(b+int(d/2))*-1+1])
    #m = max(r['middleband'][(b+d)*-1+1:(b+int(d/2))*-1+1])
    #if not util.almost_equal(l, m, 3):
    #    return False
    #l = min(r['middleband'][(b+int(d/2))*-1+1:b*-1+1])
    #m = max(r['middleband'][(b+int(d/2))*-1+1:b*-1+1])
    #if not util.almost_equal(l, m, 3):
    #    return False
    for i in range(5, b):
        l = min(r['middleband'][(i+d)*-1+1:i*-1+1])
        m = max(r['middleband'][(i+d)*-1+1:i*-1+1])
        if util.almost_equal(l, m, 5):
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
