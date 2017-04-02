
def init():
    #p = subprocess.Popen(['bash', '-c', 'nohup python3 server.py > /dev/null 2>&1 &'])
    #p.wait()

    pid_redis = get_pid_by_name('redis-server')
    if pid_redis <= 0:
        p = subprocess.Popen(['bash', '-c', 'nohup redis-server > /dev/null 2>&1 &'])
        p.wait()
        pid_redis = p.pid
        time.sleep(3)
    print('redis-server: %d' % pid_redis)

    # 以下内容暂时不改
    global cfg_file_trade
    cfg_file_trade = 'config_trade.ini'
    if os.path.exists('C:/Users/S/Desktop/config_trade.ini'):
        cfg_file_trade = 'C:/Users/S/Desktop/config_trade.ini'

    global cfg_file_trade_stocks
    cfg_file_trade_stocks = 'config_trade_stocks.ini'
    if os.path.exists('C:/Users/S/Desktop/config_trade_stocks.ini'):
        cfg_file_trade_stocks = 'C:/Users/S/Desktop/config_trade_stocks.ini'


