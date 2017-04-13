#-*- coding: utf-8 -*-

import config.config as config

def zf(quote):
    # Series.any() Series.all()
    # 20天前, 还在整理
    nday = config.ZF_NDAY
    df_quote = quote[len(quote)-nday:]['zf'] # Series
    # df_quote.mean()
    _p = len(df_quote[df_quote > config.ZF_PERCENT_MIN])/config.ZF_NDAY*100
    #if df_quote.min() > config.ZF_PERCENT_MIN and df_quote.mean() < config.ZF_PERCENT_AVG_MAX:
    if _p >= config.ZF_PERCENT_GT_MIN and df_quote.mean() < config.ZF_PERCENT_AVG_MAX:
        return True

    return False
