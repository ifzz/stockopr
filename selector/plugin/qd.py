#-*- coding: utf-8 -*-

from util.macd import ma
import config.config as config
import selector.util as util
from selector.plugin.zf import zf

def qd(quote):
    nday = config.QD_NDAY
    df_quote = quote[len(quote)-nday:]['close'] # Series
    close_min = df_quote.min()
    index_min = df_quote.argmin()
    close_max = df_quote[index_min:].max()
    close_max_all = df_quote.max()
    close = df_quote[-1]
    percent = (close_max - close_min)/close_min*100
    # df_quote.mean()
    if percent < config.QD_PERCENT_MIN or percent > config.QD_PERCENT_MAX or close_max < close_max_all:
        return False

    #print(quote['code'][-1], close_min, close_max, percent)

    return zf(quote)
