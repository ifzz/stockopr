

# 模拟盘，反馈
def add_bought_r(code):
    with mysqlcli.get_cursor() as c:
        sql = 'update {0} set b=1 where code = %s'.format(config.sql_tab_bought)
        c.execute(sql, (code,))

def add_bought(code):
    with mysqlcli.get_cursor() as c:
        key_list = ['code', 'date']
        sql = 'insert ignore into {0} ({1}) values({2})'.format(config.sql_tab_bought, ','.join(key_list), ','.join(['%s' for i in key_list]) )
        c.execute(sql, (code, datetime.date.today(),))

# 不管是否实盘建仓 一并完成操作
def del_bought_r(code):
    with mysqlcli.get_cursor() as c:
        sql = 'delete from {0} where code=%s'.format(config.sql_tab_bought)
        c.execute(sql, (code,))

# 没有实盘建仓的股票直接完成
def del_bought_maybe(code):
    with mysqlcli.get_cursor() as c:
        key_list = ['code']
        sql = 'delete from {0} where code={1} and b!=1'.format(config.sql_tab_bought, ','.join(key_list), ','.join(['%s' for i in key_list]) )
        c.execute(sql, (code,))

def add_cleared(code):
    with mysqlcli.get_cursor() as c:
        key_list = ['code', 'date']
        sql = 'insert ignore into {0} ({1}) values({2})'.format(config.sql_tab_cleared, ','.join(key_list), ','.join(['%s' for i in key_list]) )
        #sql = 'update {0} set b=2, clear_date={2} where code = {1}'.format(config.sql_tab_bought, code, datetime.date.today())
        try:
            c.execute(sql, (code, datetime.date.today(), ))
        except:
            return

    del_bought_maybe(code)

def add_trade_detail(code, op, price, count=100, account='DEFAULT'):
    with mysqlcli.get_cursor() as c:
        key_list = ['code', 'trade_date', 'op', 'price', 'count', 'account']
        sql = 'insert into {0} ({1}) values({2})'.format(
                config.sql_table_trade_detail, ','.join(key_list), ','.join(['%s' for i in key_list]) )
        c.execute(sql, (code, datetime.date.today(), 'B', price, count, account))

# op: B S
def add_trade(code, op, price, count, account='DEFAULT'):
    # 建仓 平仓 加仓 减仓
    # B: 建仓/加仓
    # S: 平仓/减仓
    if op == 'B':
        add_bought()
    elif op == 'S':
        add_cleared()
    elif op == 'P':
        add_cleared()
    elif op == 'M':
        add_cleared()
    else:
        return

# 实盘平仓
def get_to_clear():
    with mysqlcli.get_cursor() as c:
        #sql = 'select a.code from {0} as a, {1} as b where a.code = b.code and a.b = 1'.format(config.sql_tab_bought, config.sql_tab_cleared)
        sql = 'select a.code from {0} as a where a.b = 1'.format(config.sql_tab_bought)
        c.execute(sql)
        code_list = []
        r = c.fetchall()
        for i in r:
            code_list.append(i['code'])
        return code_list


