#-*- coding:utf-8 -*-

import pymysql.cursors

import config.config as config

db = config.db
db_host = config.db_host

def get_connection():
    connection = pymysql.connect(host=db_host,
        user=config.db_user,
        password=config.db_passwd,
        db=db,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)
    return connection

def get_connection_list():
    connection = pymysql.connect(host=db_host,
        user=config.db_user,
        password=config.db_passwd,
        db=db,
        charset='utf8')
    return connection

# cur.execute('SET autocommit = 0')
def get_connection_auto_commit():
    connection = pymysql.connect(host=db_host,
        user=config.db_user,
        password=config.db_passwd,
        db=db,
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True)
    return connection


# 检测连接是否正常
#def get_cursor(conn):
#    return conn.cursor()

def get_cursor():
    conn = get_connection_auto_commit()
    return conn.cursor()

def close_conn(conn, c):
    c.close()
    conn.close()

def commit_conn(conn):
    conn.commit()
import time

def test():
    pass
    #c = get_cursor()
    #c.execute('select code from basic_info where code = "600839"')
    #print(c.fetchone())
    #return c
    with get_cursor() as c:
        c.execute('select code from {0} where code = "600839"'.format(config.sql_tab_basic_info))
        print(c.fetchone())
    time.sleep(60)
if __name__ == '__main__':
    test()
    time.sleep(60)
