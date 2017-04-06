#-*- coding: utf-8 -*-

import config.config as config
from util.macd import ma

def almost_equal(m, n, almost=config.ALMOST_EQUAL):
    l = m
    if m > n:
        l = n
    if abs(m - n) * 100 / l < almost:
        return True
    return False

def gen_ma(quote, n=config.MA_NUM, l=config.MAS):
    r = []
    for i in range(n):
        r.append(ma(quote, l[i]))

    return r

def filter_quote(quote):
    if len(quote) < config.MIN:
        return True
    return False

def filer_code(code):
    if basic.sum_trade_date(code) < config.MIN:
        return True
    return False

def verify(code, dt=True):
    pass

def print_time(t):
    if int(cost/5) == 0:
        print(cost)

def print_line(a):
    if a % 100 == 0:
        n = int(a/100)
        print('{0}'.format('-'*n))
