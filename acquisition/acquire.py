#-*- encoding:utf-8 -*-

import os, sys
import time, datetime
import xlrd
import urllib.request
import json

import socket

import util.mysqlcli as mysqlcli
import util.basic as basic
import util.tx as tx
import util.quote_db as quote_db

# timeout in seconds
timeout = 5
socket.setdefaulttimeout(timeout)

def save_stock_basic_info(xlsfile):
    stock_list = tx.get_stock_list(xlsfile)
    stock_list = sorted(stock_list)
    basic.save_stock_list_into_db(stock_list)

def update_stock_basic_info(xlsfile):
    # http://stock.gtimg.cn/data/get_hs_xls.php?id=ranka&type=1&metric=chr
    stock_list = tx.get_stock_list(xlsfile)
    stock_list = sorted(stock_list)
    basic.update_stock_list_into_db(stock_list)

def _save_quote(_xls, dt=None):
    val_list = tx.get_quote(_xls)
    #print(val_list)
    quote_db.insert_into_quote(val_list)

# 指数
def save_sh_index_trade_info():
    val = quote_db.get_price_urllib('999999')
    if val:
        quote_db.insert_into_quote([val,])

def save_stock_trade_info_tx():
    _xls = tx.download_quote_xls()
    if _xls:
        _save_quote(_xls)
        save_stock_basic_info(_xls)
        today = datetime.date.today()
        if today.day == 1:
            update_stock_basic_info(_xls)

def save_quote():
    save_sh_index_trade_info()
    save_stock_trade_info_tx()

_save_quote('test/2017-04-02-14-31_ranka.xls')

if __name__ == '__main__':
    if not basic.istradeday():
        pass
        #exit(0)
    save_quote()
