#-*- encoding:utf-8 -*-

import os, sys
import time, datetime
import xlrd
import urllib.request
import json

import socket

import config.config as config
import util.mysqlcli as mysqlcli
import acquisition.basic as basic
import acquisition.tx as tx
import acquisition.wy as wy
import acquisition.quote_db as quote_db

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

# 指数
def save_sh_index_trade_info():
    val = quote_db.get_price_urllib('999999')
    if val:
        quote_db.insert_into_quote([val,])

def save_quote_tx():
    _xls = tx.download_quote_xls()
    if _xls:
        val_list = tx.get_quote(_xls)
        quote_db.insert_into_quote(val_list)
        save_stock_basic_info(_xls)
        today = datetime.date.today()
        if today.day == 1:
            update_stock_basic_info(_xls)

from sqlalchemy import create_engine

def save_quote_wy():
    df_quote = wy.get_quote()

    with mysqlcli.get_cursor() as c:
        try:
            # clear temp table
            c.execute('truncate table temp_quote')

            # MySql connection in sqlAlchemy
            engine = create_engine('mysql://{0}:{1}@127.0.0.1:3306/stock?charset=utf8'.format(config.db_user, config.db_passwd))
            connection = engine.connect()

            # Do not insert the row number (index=False)
            df_quote.to_sql(name='temp_quote', con=engine, if_exists='append', index=False, chunksize=20000)
            #connection.close()

            sql_str = "select code, close, high, low, open, yestclose from quote where code in ('000001', '000002', '000003', '000004', '000005') and trade_date in (select max(trade_date) from quote);"
            c.execute(sql_str)
            r1 = c.fetchall()

            sql_str = "select code, close, high, low, open, yestclose from temp_quote where code in ('000001', '000002', '000003', '000004', '000005') and trade_date in (select max(trade_date) from temp_quote);"
            c.execute(sql_str)
            r2 = c.fetchall()

            r1_sorted = sorted(r1, key = lambda x:x['code'])
            r2_sorted = sorted(r2, key = lambda x:x['code'])
            if r1_sorted != r2_sorted:
                c.execute('insert into temp_quote_test select * from temp_quote;')
                pass
            else:
                print('not trade day')
        except Exception as e:
            print(e)

save_quote_wy()

def save_quote():
    save_sh_index_trade_info()
    #save_quote_tx()
    save_quote_wy()


if __name__ == '__main__':
    if not basic.istradeday():
        pass
        #exit(0)
    save_quote()