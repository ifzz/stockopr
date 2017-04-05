#-*- coding: utf-8 -*-
'''
1 横盘时间
'''

import sys
import time

import numpy as np
import pandas

import acquisition.basic as basic
import acquisition.quote_db as price

import selector.plugin.hp as hp
import selector.plugin.hp_p as hp_p
import selector.plugin.hp_pp as hp_pp
import selector.plugin.hp_ppp as hp_ppp

import selector.plugin.second_wave as second_wave
import selector.plugin.second_wave2 as second_wave2

import selector.plugin.tp as tp

import selector.plugin.z as z
import selector.plugin.dz as dz

import selector.plugin.d as d
import selector.plugin.dd as dd

import selector.selected as selected

import util.util as util

from util.macd import ma
from util.macd import bbands
from util.macd import dmi
from util.macd import macd
from util.macd import sar

#import future

# 横盘 第二波 突破 涨 跌 大涨 大跌
selector = {'hp':hp, 'hp_p':hp_p, 'hp_pp':hp_pp, 'hp_ppp':hp_ppp, '2nd':second_wave, '2nd2':second_wave2, 'tp':tp, 'z':z, 'dz':dz, 'd':d, 'dd':dd, 'test':test} #'dt':dt,

def filter_quote(quote):
    if len(quote) < MIN:
        return True
    return False

def filer_code(code):
    if basic.sum_trade_date(code) < MIN:
        return True
    return False

def test(quote):
    return
    r = gen_ma(quote)
    r_ = r[0].shift(1)
    print(r[0].ma[-3:], r_.ma[-3:])
    b = r[0].ma < r_.ma
    print(b.all())
    exit(0)
    r = dt_ma(quote, last_n_maN=5)
    exit(0)
    ht_ma(quote)
    exit(0)

def verify(code, dt=True):
    pass

def print_time(t):
    if int(cost/5) == 0:
        print(cost)

def print_line(a):
    if a % 100 == 0:
        n = int(a/100)
        print('{0}'.format('-'*n))

def select(cls='hp'):
    t1 = time.time()
    code_list = basic.get_all_stock_code()
    #code_list = future.get_future_contract_list()
    #print(code_list)
    #code_list = ['600886']
    a = len(code_list)
    print('+++ {0} {1} +++\n'.format(a, cls))

    pre_cost = 0
    cost = 0

    s = 0
    for code in code_list:
        a -= 1
        #print_line(a)
        cost = int(time.time()-t1)
        if cost != pre_cost:
            pre_cost = cost
            if cost % 5 == 0:
                print('{0}s\t{1}'.format(cost, a))

        p = price.get_price_info_df_db(code, 500, '', T)
        if filter_quote(p):
            continue

        rc = selector.get(cls)(p)
        if rc:
            s += 1
            print('{2}{0} {1}'.format(code, basic.get_stock_name(code), ' '*50))
            #print('{2}{0} {1}'.format(code, basic.get_future_name(code), ' '*50))
            # insert into selected
            selected.add_selected(code)

    t2 = time.time()
    print('\n+++ {0} +++\n+++ {1} +++'.format(s, int(t2 - t1)))
    print('\n计划你的交易 交易你的计划\n')

select('2nd2')

if __name__ == '__main__':
    #select('hp')
    #select('hp_p')
    #select('hp_pp')
    #select('tp')
    #select('2nd')
    select('2nd2')
    #select('z')
    #select('d')
    #select('dd')
    #select('z')
    #select('dz')
