from config.confighandler import ConfigHandler
ch = ConfigHandler('config/config.ini', 'db')
db_host = ch.db_host
db = ch.db
db_user = ch.db_user
db_passwd = ch.db_passwd
sql_tab_basic_info = ch.sql_table_basic_info
sql_tab_quote = ch.sql_table_quote
sql_tab_selected = ch.sql_table_selected
sql_tab_selected_history = ch.sql_table_selected_history
sql_tab_bought = ch.sql_table_bought
sql_tab_cleared = ch.sql_table_cleared
sql_tab_trade_detail=ch.sql_table_trade_detail
sql_tab_trade_detail_history=ch.sql_table_trade_detail_history

charg = ConfigHandler('config/config.ini', 'arg')
check_per_sec = charg.check_per_sec

###

debug = True
debug = False
monitoring = False
monitoring = True
if debug:
    monitoring = True

#data_config_trade
auto_active_wnd = 1
auto_open_stock_graph_half = 1
auto_open_stock_graph_full = 0
auto_trade_half = 1
auto_trade_full = 0

class cfg:
    auto_active_wnd = 1
    auto_open_stock_graph_half = 1
    auto_open_stock_graph_full = 0
    auto_trade_half = 1
    auto_trade_full = 0

def cfg_auto_active_wnd(val):
    cfg.auto_active_wnd = val
def cfg_auto_open_stock_graph_half(val):
    cfg.auto_open_stock_graph_half = val
def cfg_auto_open_stock_graph_full(val):
    cfg.auto_open_stock_graph_full = val
def cfg_auto_trade_half(val):
    cfg.auto_trade_half = val
def cfg_auto_trade_full(val):
    cfg.auto_trade_full = val

dict_data_config_trade = {'auto_active_wnd':cfg_auto_active_wnd,
                         'auto_open_stock_graph_half':cfg_auto_open_stock_graph_half,
                         'auto_open_stock_graph_full':cfg_auto_open_stock_graph_full,
                         'auto_trade_half':cfg_auto_trade_half,
                         'auto_trade_full':cfg_auto_trade_full}

def cfg_data(key, val):
    dict_data_config_trade.get(key)(int(val))

'''
注意,
通达信与中信证券交易软件操作界面并不相同
中信证券光标会自动跳转到'买入数量'
国金证券还没有测试
'''

pid = 0
hwnd = 0
start_time_am = 0
start_time_pm = 0

# 转向 逆转 突破 异动
indicator_h = {'zx_up':4, 'lz_up':2, 'tp_up':1, 'zx_down':-4, 'lz_down':-2, 'tp_down':-1, 'yd_up':1, 'yd_down':-1}
indicator_l = {'zx_up':2, 'lz_up':1, 'tp_up':0.5, 'zx_down':-2, 'lz_down':-1, 'tp_down':-0.5, 'yd_up':1, 'yd_down':-1}
if debug:
    indicator = indicator_h
else:
    indicator = indicator_l

if debug:
    wait_time_ll = 0.1
    wait_time_l = 0.1
    wait_time_m = 0.1
    wait_time_s = 0.1
    wait_time_ss = 0.1
    alert_interval_time = 1
    alert_startup_time = 1
else:
    wait_time_ll = 0.5 #10
    wait_time_l = 0.5 #5
    wait_time_m = 0.5 #1
    wait_time_s = 0.5
    wait_time_ss = 0.1
    alert_interval_time = 60
    alert_startup_time = 300


wait_time = wait_time_m

mouse_clk_x = 800
mouse_clk_y = 300

dbip='127.0.0.1'
dbport=6379
dbpassword=''

cmd_buy_tdx = '221'
cmd_sell_tdx = '223'

cfg_file_trade = ''
cfg_file_trade_stocks = ''

stocks_realtime_info = {}

ChinaStockIndexList = [
    "000001", # sh000001 上证指数
    "399001", # sz399001 深证成指
    "000300", # sh000300 沪深300
    "399005", # sz399005 中小板指
    "399006", # sz399006 创业板指
    "000003",  # sh000003 B股指数
]

accounts = {'tdx_zxs':{'pid':'', 'hwnd':'', 'hwnd_name':'', 'exe_path':''},
            'ths_gjs':{'pid':'', 'hwnd':'', 'hwnd_name':'', 'exe_path':'D:\\BIN\\全能行证券交易终端\\xiadan.exe'},
            'ths_gjl':{'pid':'', 'hwnd':'', 'hwnd_name':'', 'exe_path':'D:\\BIN\\weituo\\国金证券\\xiadan.exe'}, #'D:\\BIN\\weituo\\国金证券\\xiadan.exe'},
            'hs_s':{'pid':'', 'hwnd':'', 'hwnd_name':'', 'exe_path':'D:\\BIN\\HOMS钱江版(独立委托版)\\Trading.exe'}}

dict_exe_path_account = {'D:\\BIN\\全能行证券交易终端\\xiadan.exe':'ths_gjs',
                'D:\\BIN\\weituo\\国金证券\\xiadan.exe':'ths_gjl',
                'D:\\BIN\\HOMS钱江版(独立委托版)\\Trading.exe':'hs_s'}

stages = ['3', '35', '354', '352', '3523', '3526', '35264', '35261', '352613', '352614',
          '4', '42', '423', '425', '4254', '4251', '42513', '42516', '425164', '425163']


key_list = ['code', 'name', 'trading_date', 'open', 'high', 'low', 'close', 'volume', 'turnover']

'''
selector
'''
T = 'W'
T = 'D'
D_MIN = 250
W_MIN = 52
MIN = D_MIN if T == 'D' else W_MIN

DZ_MIN = 120 if T == 'D' else 25
DD_MIN = 120 if T == 'D' else 25

# 1.1^5 = 1.61
DZ_PERCENT_LIMIT = 11 if T == 'D' else 61
# 0.9^5 = 59.04
DD_PERCENT_LIMIT = 11 if T == 'D' else 41

HP_BOLL_BACK = 20 if T == 'D' else 4
HP_BOLL_DURATION = 60 if T == 'D' else 12

HP_DAY = 1
HP_DURATION = -1
HP_FIRST_N_MA = 5

ALMOST_EQUAL = 1
MA_NUM = 5
MAS = [5, 10, 20, 30, 60]



DT_DAY = 1
DT_LAST_N_MA = 4

# 多头最小涨幅, (ma5 - ma60)/ma60 * 100
DT_MIN_UP_P = 5

# boll中线, 10天以前
DT_BOLL_DAY = 10
DT_BOLL_DAY_AGO = 60

DT_SAR_DAY = 5


HT_MA_N = 10
HT_RANGE = 10


SECOND_DAY = 1
SECOND_LAST_N_MA = 4


TP_MA_N = 20
TP_RANGE = 5


D_PERCENT_EXP = 15
D_NDAY = 5


Z_PERCENT_EXP = 15
Z_NDAY = 5

