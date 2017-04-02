
def init_win():
    if get_pid_by_name('redis-server.exe') <= 0:
        subprocess.Popen('D:\\DEVBIN\\redis-2.8.19\\redis-server.exe')

    global cfg_file_trade
    cfg_file_trade = 'config_trade.ini'
    if os.path.exists('C:/Users/S/Desktop/config_trade.ini'):
        cfg_file_trade = 'C:/Users/S/Desktop/config_trade.ini'

    global cfg_file_trade_stocks
    cfg_file_trade_stocks = 'config_trade_stocks.ini'
    if os.path.exists('C:/Users/S/Desktop/config_trade_stocks.ini'):
        cfg_file_trade_stocks = 'C:/Users/S/Desktop/config_trade_stocks.ini'


