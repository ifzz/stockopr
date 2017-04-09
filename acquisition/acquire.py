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
import acquisition.quote_www as quote_www

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
    val = quote_www.get_price_urllib('999999')
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

# 网易行情接口
def save_quote_wy():
    df_quote = wy.get_quote()

    # 修改数据库
    '''
    update quote set
    percent=FORMAT(percent*100, 2), hs=FORMAT(hs*100, 2), lb=FORMAT(lb, 2),
    wb=FORMAT(wb*100, 2), zf=FORMAT(zf*100, 2), five_minute=FORMAT(five_minute*100, 2)
    where trade_date >= '2017-04-05 00:00:00';
    '''
    # 部分值转换
    key_list = ['PERCENT', 'HS', 'WB', 'ZF', 'FIVE_MINUTE']
    for key in key_list:
        df_quote[key] = round(df_quote[key]*100, 2)
    key = 'LB'
    df_quote[key] = round(df_quote[key], 2)
    #print(df_quote[df_quote['CODE'] == '600839'])

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
                c.execute('insert into quote select * from temp_quote;')
                #c.execute('insert into temp_quote_test select * from temp_quote;')
            else:
                print('not trade day')
        except Exception as e:
            print(e)

def save_quote():
    save_sh_index_trade_info()
    #save_quote_tx()
    save_quote_wy()


if __name__ == '__main__':
    if not basic.istradeday():
        pass
        #exit(0)
    save_quote()
