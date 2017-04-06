#-*- coding: utf-8 -*-
#import toolkit.wy_save_history_multiprocess
import util.macd
#import acquisition.wy as wy

def test_save_quote():
    import acquisition.acquire as acquire
    acquire.save_quote()

def test_select():
    import selector.selector as selector
    import acquisition.basic as basic
    code_list = selector.select('z')
    for code in code_list:
        print(code, basic.get_stock_name(code))

if __name__ == '__main__':
    #test_save_quote()
    test_select()
