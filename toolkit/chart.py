import matplotlib.pyplot as plt
import sys

sys.path.append(".")

from acquisition import quote_db

'''
http://chartapi.finance.yahoo.com/instrument/1.0/000001.sz/chartdata;type=quote;range=1m/csv
'''

def show(code, n=250):
    r = quote_db.get_price_info_df_db(code, n)
    n = n if len(r) >= n else len(r)

    x = [i for i in range(n)]
    close = r['close'][-1]
    y = round((r['close'] - close)/close*100, 2)
    #y = r['close']

    plt.axhline(y=0, color='b')
    plt.grid(True)
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())
    plt.plot(x,y)
    plt.show()

if __name__ == '__main__':
    show('600570')
