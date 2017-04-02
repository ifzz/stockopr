

def add_selected_history(code):
    with mysqlcli.get_cursor() as c:
        sql = 'select added_date, class, rank from {0} where code = "{1}" order by added_date desc'.format(config.sql_tab_selected, code)
        c.execute(sql)
        r = c.fetchone()
        if not r:
            return

        sql = 'insert into {0} (code, added_date, class, rank) values("{1}", "{2}", "{3}", {4})'.format(config.sql_tab_selected_history,
                code, str(r['added_date']), r['class'], r['rank'])
        c.execute(sql)

def remove_selected(code):
    with mysqlcli.get_cursor() as c:
        sql = 'delete from {0} where code = "{1}"'.format(config.sql_tab_selected, code)
        c.execute(sql)

def remove_selected_keep_history(code):
    with mysqlcli.get_cursor() as c:
        add_selected_history(code)
        sql = 'delete from {0} where code = "{1}"'.format(config.sql_tab_selected, code)
        c.execute(sql)

# HP, 横盘
def add_selected(code, cls='HP', rank=9):
    with mysqlcli.get_cursor() as c:
        sql = 'select added_date from {0} where code = "{1}" order by added_date desc'.format(config.sql_tab_selected, code)
        c.execute(sql)
        r = c.fetchone()
        if r:
            # r['added_date'], datetime.date
            #tm = time.strptime(r['added_date'], '%Y-%m-%d')
            #t = time.mktime(tm)
            #d = datetime.date.fromtimestamp(t)
            # datetime.timedelta
            if (datetime.date.today() - r['added_date']).days <= 5:
                return
            remove_selected_keep_history(code)
        sql = 'insert into {0} (code, added_date, class, rank) values("{1}", current_date(), "{2}", {3})'.format(config.sql_tab_selected, code, cls, rank)
        # code varchar(8), added_date date, class varchar(8), rank integer
        c.execute(sql)

