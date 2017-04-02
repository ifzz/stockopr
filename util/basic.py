#-*- encoding: utf-8 -*-

#from util import get_pid_by_name
import subprocess
import os
import time
from datetime import date
import datetime
import util.mysqlcli as mysqlcli
import util.quote_www as price
import config.config as config

def get_all_stock_code():
    with mysqlcli.get_cursor() as c:
        #sql = 'SELECT DISTINCT code FROM {0}'.format(config.sql_tab_quote)
        sql = "SELECT code FROM {0} where type = 'A股'".format(config.sql_tab_basic_info)
        c.execute(sql)
        stock_code_list = c.fetchall()

        return [code['code'] for code in stock_code_list]

# insert new row
# stock_list[(code, name), ...]
def save_stock_list_into_db(stock_list):
    with mysqlcli.get_cursor() as cursor:
        sql_fmt = u"INSERT INTO basic_info (code, name) VALUES ('{}', '{}')"
        for code, name in stock_list:
            sql = sql_fmt.format(code, name)
            try:
                cursor.execute(sql, None)
            except pymysql.err.IntegrityError as e:
                pass
            except Exception as e:
                print(e)

# update old row
# stock_list[(code, name), ...]
def update_stock_list_into_db(stock_list):
    with mysqlcli.get_cursor() as cursor:
        # Create a new record
        #sql_fmt = u"INSERT INTO basic_info (code, name) VALUES ('{}', '{}') ON DUPLICATE KEY update name = {}"
        sql_ins = "INSERT INTO basic_info (code, name) VALUES ('{}', '{}')"
        sql_sel = 'select name from basic_info where code = "{0}"'
        sql_upd = 'update basic_info set name = "{1}" where code = "{0}"'
        for code, name in stock_list:
            #sql = sql.format(code, name.decode('unicode-escape'))
            try:
                sql = sql_sel.format(code)
                n = cursor.execute(sql, None)
                if n == 0:
                    sql = sql_ins.format(code, name)
                    cursor.execute(sql, None)
                    continue
                r = cursor.fetchone()
                if r['name'] == name:
                    continue
                sql = sql_upd.format(code, name)
                #sql = sql_fmt.format(code, name)
                cursor.execute(sql, None)
            except Exception as e:
                print(e) #(1062, "Duplicate entry '603999' for key 'PRIMARY'")

def get_selected_stock_code():
    code_list = []
    with mysqlcli.get_cursor() as c:
        sql = 'select code from {0}'.format(config.sql_tab_selected)
        c.execute(sql)
        r = c.fetchall()
        for item in r:
            code_list.append(item['code'])
        return code_list

def sum_trade_date(code):
    with mysqlcli.get_cursor() as c:
        sql = 'select count(code) from {0} where code = "{1}"'.format(config.sql_tab_quote, code)
        c.execute(sql)
        r = c.fetchone()
        return list(r.values())[0]

def save_stock_name():
    stock_code_list = get_all_stock_code()
    val_list = []

    conn = mysqlcli.get_connection()
    c = mysqlcli.get_cursor(conn)
    for i, code in enumerate(stock_code_list):
        if i % 3 ==0:
            stock_info = price.getChinaStockIndividualPriceInfo(code)
        elif i % 3 == 1:
            stock_info = price.getChinaStockIndividualPriceInfoTx(code)
        else:
            stock_info = price.getChinaStockIndividualPriceInfoWy(code)

        if not stock_info:
            print(code)
            continue

        try:
            #val_list.append(tuple([code, stock_info['name']]))
            time.sleep(0.1)
            sql = 'insert into {0} (code, name) values ("%s", "%s")'.format(config.sql_tab_basic_info) % tuple([code, stock_info['name']])
            c.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)

    #for val in val_list:
    #    print(val)
    #sql = 'insert into basic_info (code, name) values (%s, %s)'
    #c.executemany(sql, val_list)
    #conn.commit()
    c.close()
    conn.close()

# 没有调用
def update_stock_name():
    stock_code_list = get_all_stock_code()
    val_list = []

    conn = mysqlcli.get_connection()
    c = mysqlcli.get_cursor(conn)
    for i, code in enumerate(stock_code_list):
        try:
            code_i = int(code)
            if code_i >= 600000:
                continue
            #val_list.append(tuple([code, stock_info['name']]))
            sql = 'update {0} set code = "%s" where code = "%d"'.format(config.sql_tab_basic_info) % tuple([code, code_i])
            c.execute(sql)
            conn.commit()
        except Exception as e:
            print(e)

    #for val in val_list:
    #    print(val)
    #sql = 'insert into basic_info (code, name) values (%s, %s)'
    #c.executemany(sql, val_list)
    #conn.commit()
    c.close()
    conn.close()

def get_stock_name(code):
    with mysqlcli.get_cursor() as c:
        try:
            sql = 'select name from {0} where code = "{1}"'.format(config.sql_tab_basic_info, code)
            c.execute(sql)
            #name = c.fetchall()
            r = c.fetchone()
            return r['name']
        except Exception as e:
            print(e)

def get_future_name(code):
    if code.find('1') > 0:
        code = code[:-4]
    elif code[-1] == '0':
        code = code[:-1]

    with mysqlcli.get_cursor() as c:
        try:
            sql = 'select name from future_variety where code = "{1}"'.format(config.sql_tab_basic_info, code)
            c.execute(sql)
            #name = c.fetchall()
            r = c.fetchone()
            return r['name']
        except Exception as e:
            print(e)



if __name__ == '__main__':
    pass
    add_selected_history('600674')
    exit(0)
    print(get_stock_name('600839'))
    exit(0)
    add_bought('600839')
    add_cleared('600839')
    r = get_to_clear()
    print(r)
    #add_trade('600839', 'B', 1, 100)
    #print(get_code_list_monitored())
    #print(sum_trading_date('600839'))
    #add_monitor('600839')
    # update_stock_name()
