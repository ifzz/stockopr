#-*- coding: utf-8 -*-

import os
import time
import datetime
import urllib.request

import xlrd

url = 'http://stock.gtimg.cn/data/get_hs_xls.php?id=ranka&type=1&metric=chr'

def init():
    if not os.path.exists('data/xls'):
        os.makedirs('data/xls')

def _download_quote_xls():
    _dataUrl = url
    trade_date = str(datetime.date.today())
    _xls = 'data/xls/{0}.xls'.format(trade_date)

    if os.path.exists(_xls):
        print('existed')
        return

    try_ = 5
    while try_ > 0:
        try:
            urllib.request.urlretrieve(_dataUrl, _xls)
            break
        except Exception as e:
            try_ -= 1
            if try_ == 0:
                # TODO
                raise e
            time.sleep(1)
            continue

    return _xls

def download_quote_xls():
    init()
    _xls = _download_quote_xls()
    if not _xls:
        return

    data = xlrd.open_workbook(_xls) #注意这里的workbook首字母是小写
    sheet = data.sheet_names()[0]
    table = data.sheet_by_name(sheet)

    # ['数据更新时间', '12-25 15:15:12', '', '', '', '', '', '', '', '', '', '', '']
    update_day =table.row_values(0)[1].split()[0]
    dt = str(datetime.date.today())
    if dt.find(update_day) < 0:
        os.remove(_xls)
        print('not today, xls removed')
        return

    return _xls

# return: [(code, name),]
def get_stock_list_from_quote_xls(_xls):
    stock_list = []

    #打开excel
    data = xlrd.open_workbook(_xls) #注意这里的workbook首字母是小写

    #查看文件中包含sheet的名称
    sheets = data.sheet_names()
    sheet = sheets[0]

    #得到第一个工作表，或者通过索引顺序 或 工作表名称
    table = data.sheets()[0]
    table = data.sheet_by_index(0)
    table = data.sheet_by_name(sheet)
    #获取行数和列数
    #nrows = table.nrows
    #ncols = table.ncols
    #获取整行和整列的值（数组）
    i = 0
    table.row_values(i)
    table.col_values(i)
    #循环行,得到索引的列表
    B = False
    for rownum in range(table.nrows):
        row = table.row_values(rownum)
        if not B and not row[i].startswith('s'):
            continue

        code = row[0][2:]
        name = row[1]
        #ex = 1 if code >= 600000 else 2

        #stock_list.append((code, name, ex))
        stock_list.append((code, name))

        continue

        break
    ##单元格
        #cell_A1 = table.cell(0,0).value
        ##分别使用行列索引
        #cell_A1 = table.row(0)[0].value
        #cell_A2 = table.col(1)[0].value

    return stock_list

def check_format(row):
    #if len(row) != 13:
    #    return False
    if row != ['代码', '名称', '最新价', '涨跌幅', '涨跌额', '买入', '卖出', '成交量', '成交额', '今开', '昨收', '最高', '最低']:
        return False
    return True

def get_quote(xlsfile, dt=None):

    #打开excel
    data = xlrd.open_workbook(xlsfile) #注意这里的workbook首字母是小写

    #查看文件中包含sheet的名称
    sheets = data.sheet_names()
    sheet = sheets[0]

    #得到第一个工作表，或者通过索引顺序 或 工作表名称
    table = data.sheets()[0]
    table = data.sheet_by_index(0)
    table = data.sheet_by_name(sheet)

    if not check_format(table.row_values(1)):
        raise Exception('xls format changed...')

    #获取行数和列数
    #nrows = table.nrows
    #ncols = table.ncols
    #获取整行和整列的值（数组）
    #循环行,得到索引的列表
    trade_date = None
    # ['数据更新时间', '12-25 15:15:12', '', '', '', '', '', '', '', '', '', '', '']
    update_day =table.row_values(0)[1].split()[0]
    if dt == None:
        dt = str(datetime.date.today())
    if dt.find(update_day) < 0:
        print(dt, update_day, 'not today\'s quote')
        #os.remove(xlsfile)
        return

    trade_date = dt
    val_many = []
    for rownum in range(table.nrows):
        row = table.row_values(rownum)
        if not row[0].startswith('s'):
            continue

        print(row[0])

        key_xls = ['代码', '名称', '最新价', '涨跌幅', '涨跌额', '买入', '卖出', '成交量', '成交额', '今开', '昨收', '最高', '最低', '日期']
        key_dict = {'代码':'code', '名称':'', '最新价':'close', '涨跌幅':'', '涨跌额':'',
                '买入':'', '卖出':'', '成交量':'volume', '成交额':'turnover',
                '今开':'open', '昨收':'', '最高':'high', '最低':'low',
                '日期':'trade_date'}
        row.append(trade_date)
        row[0] = row[0][2:]

        #AttributeError: 'dict' object has no attribute 'iteritems'
        key_list = ['code', 'trade_date', 'open', 'high', 'low', 'close', 'volume', 'turnover']
        indice = [0, 13, 9, 11, 12, 2, 7, 8] #subscript
        fmt_list = ['%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s']
        val_list = []
        volume = row[7]
        if int(volume) <= 0:
            #print(row[0], '停牌')
            continue
        row[7] *= 100

        for i, idx in enumerate(indice):
            val_list.append(row[idx])
            if key_list[i] != key_dict[key_xls[idx]]:
                exit(0)
            #print('{0}\t{1}\t{2}'.format(key_list[i], key_xls[idx], row[idx]))


        val = tuple(val_list)
        val_many.append(val)

    # print(sql_str % tuple(val_list))

    return val_many


if __name__ == '__main__':
    download_xls()
