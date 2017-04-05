#-*- coding: utf-8 -*-

import pandas
import util.util as util

# n天跌幅
# 10天跌15%, ma60向上
def d(quote, percent_exp=config.D_PERCENT_EXP, nday=config.D_NDAY):
    quote = quote[-1*nday:]
    if len(quote) < nday:
        return False

    percent = 100*(quote['close'] - quote['close'].shift(1))/quote['close'].shift(1)
    #percent = percent[np.isfinite(percent)]
    percent = percent[pandas.notnull(percent)]
    #df.dropna()
    #df.dropna(how='all')

    if min(percent) < -1*config.DD_PERCENT_LIMIT:
        return False

    percent = 100 * (quote['close'][-1] - max(quote['close'])) / max(quote['close'])
    #max_percent = 1 - 0.9**nday
    #if max_percent < percent:
    #    continue
    if percent*-1 > percent_exp:
        from datetime import datetime
        if config.T == 'W':
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
    return d(quote, 50, config.DD_MIN)
