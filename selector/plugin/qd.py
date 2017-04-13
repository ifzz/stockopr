#-*- coding: utf-8 -*-

from util.macd import ma
import config.config as config
import selector.util as util
from selector.plugin.zf import zf

def qd(quote):
    nday = config.QD_NDAY
    df_quote = quote[len(quote)-nday:]['close'] # Series
    index_min = df_quote.argmin()
    close_min = df_quote[index_min]

    index_min_max = df_quote[index_min:].argmax()
    close_min_max = df_quote[index_min_max]

    index_min_max_min = df_quote[index_min_max:].argmin()
    close_min_max_min = df_quote[index_min_max_min]

    close_max_all = df_quote.max()
    close = df_quote[-1]
    percent_max = (close_min_max - close_min)/close_min*100
    percent_ht_max = (close_min_max - close_min_max_min)/close_min_max*100
    percent = (close - close_min)/close_min*100
    #print(percent_max, percent_ht_max)
    # df_quote.mean()
    if percent_max < config.QD_PERCENT_MIN or percent_max > config.QD_PERCENT_MAX or percent_ht_max > config.QD_PERCENT_HT_MAX or close_min_max < close_max_all:
        return False

    #print(quote['code'][-1], close_min, close_max, percent)

    return zf(quote)
