#-*- coding: utf-8 -*-

import pandas

import config.config as config
import util.util as util
import util.dt as util_dt

Z_PERCENT_EXP = 15
Z_NDAY = 5

# n天涨幅
def z(quote, percent_exp=config.Z_PERCENT_EXP, nday=Z_NDAY):
    quote = quote[-1*nday:]
    #quote = price.get_price_info_df_db(code, nday)
    if len(quote) < nday:
        return False

    quote_close_yest = quote['close'].shift(1)
    percent = 100*(quote['close'] - quote_close_yest)/quote_close_yest
    percent = percent[pandas.notnull(percent)]
    if max(percent) > config.DZ_PERCENT_LIMIT:
        return False

    quote_close_min = min(quote['close'])
    quote_close_max = max(quote['close'])
    percent = 100 * (quote['close'][-1] - quote_close_min) / quote_close_min
    #percent = 100 * (quote_close_max - quote_close_min) / quote_close_min
    #max_percent = 1.1**nday - 1
    #if max_percent < percent:
    #    continue

    if percent > percent_exp:
        _d = util_dt.dt64_to_dt(quote.index.values[-1])
        if util.pause_trade(_d):
            #print('{0}\t{1}\t{2} %(停牌)'.format(code, name, round(percent, 2)))
            return False
    else:
        return False

    return True

def dz(quote):
    return z(quote, 100, config.DZ_MIN)
