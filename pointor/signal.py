#-*- encoding: utf-8 -*-

import time
import datetime

import copy

import acquisition.quote_db as quote_db
import acquisition.quote_www as quote_www

import pointor.signal_gd as signal_gd
import dealer.bought as basic

def mktime(_datetime):
    # time.mktime((tm_today.tm_year, tm_today.tm_mon, tm_today.tm_mday, 9, 30, 0, 0, 0, 0))
    return int(time.mktime(_datetime.timetuple()))

def recognize(price_info_df):
    price_info_df_last = price_info_df[-1:]
    #price = price_info_df_last.get_values()
    r = signal_gd.gold_dead(price_info_df)
    if r == 'B':
        #trade_signal_indicator(None, 0)
        # add to bought
        basic.add_bought(price_info_df_last['code'][0])
        basic.add_trading_detail(price_info_df_last['code'][0], 'B', price_info_df_last['close'][0], 100, 'ZXZQ')
    elif r == 'S':
        #trade_signal_indicator(None, 0)
        # add to cleared
        basic.add_cleared(price_info_df_last['code'][0], price_info_df_last['close'][0], 100, 'ZXZQ')
        basic.add_trading_detail(price_info_df_last['code'][0], 'S', price_info_df_last['close'][0], 100, 'ZXZQ')
    else:
        pass

# 交易日14:45执行, 确定需要交易的股票
def check_signal(code):
    price_rt = quote_www.getChinaStockIndividualPriceInfoWy(code)
    #key_list = ['code', 'trading_date', 'open', 'high', 'low', 'close', 'volume', 'turnover']
    key_list = ['code', 'open', 'high', 'low', 'close', 'volume', 'turnover']

    duration = 60
    price_info_df = quote_db.get_price_info_df_db(code, duration)

    import pandas as pd
    import numpy as np
    dates = pd.date_range(price_rt['trade_date'], periods=1)
    price_info = pd.DataFrame(np.array([[float(price_rt[key]) for key in key_list]]), index=dates, columns=list(key_list))
    price_info_df = price_info_df.append(price_info)

    recognize(price_info_df)
