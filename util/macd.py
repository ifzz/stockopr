#-*- encoding: utf-8 -*-

from talib.abstract import MACD, MACDEXT, MACDFIX
from talib.abstract import CCI
from talib.abstract import SAR
from talib.abstract import RSI
from talib.abstract import MA
from talib.abstract import EMA
from talib.abstract import SMA
#from talib.abstract import DMA
#from talib.abstract import TMA
from talib.abstract import WMA
from talib.abstract import BBANDS
from talib.abstract import PLUS_DI
from talib.abstract import MINUS_DI
from talib.abstract import ADX
from talib.abstract import ADXR
from talib.abstract import ATR
from talib.abstract import STOCH
from talib.abstract import STOCHF

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#import util.quote_db as price

'''
MACD: (12-day EMA - 26-day EMA)
Signal Line: 9-day EMA of MACD
MACD Histogram: MACD - Signal Line
note: macd histogram * 2 maybe better
'''
'''
1 加监控:
'''

macd_threshold_hp = 0.2 #
macd_threshold_0 = 0.03 # 高价股与低价股 相同走势 macd 值相差很大
B = 'B'
S = 'S'
N = ''

# note that all ndarrays must be the same length!
inputs = {
    #'open': np.random.random(100),
    #'high': np.random.random(100),
    #'low': np.random.random(100),
    'close': np.random.random(100),
    #'volume': np.random.random(100)
}

def round(f, n):
    return float('%.{0}f'.format(n) % (f))

def adjust(df, prices):
    return df

    #n = len(df)
    low = pd.rolling_min(prices['low'], 1)
    fillval = low[-1]
    low.fillna(fillval, inplace=True)
    #low = pd.expanding_min(prices['low'], 5)
    price = prices['close'][-1]
    # pandas 太霸气了 这样运算都可以
    return df / (price - low) * 100 # 换算成比例(涨跌幅度)
    #return (df - low) / (price - low) * 100 # 换算成比例(涨跌幅度)
    #return (df) / (price) * 100 # 换算成比例(涨跌幅度)

def adjust_none(val):
    if val:
        return val
    return ''

def ma(prices, n=5):
    #df = pd.DataFrame(prices.loc[:,'close'])
    df = pd.DataFrame()
    df['ma'] = MA(prices, timeperiod=n)

    return df

# Moving Average Convergence/Divergence Oscillator
'''
EMA: Exponential Moving Average

MACD Line: (12-day EMA - 26-day EMA)
Signal Line: 9-day EMA of MACD Line
MACD Histogram: MACD Line - Signal Line
'''
# close
def macd(prices):
    df = MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9)
    #print(type(df)) # <class 'pandas.core.frame.DataFrame'>
    #return adjust(df, prices)

    return df

# stop and reverse
# Parabolic Time/Price System
'''
Rising SAR

Prior SAR: The SAR value for the previous period.

Extreme Point (EP): The highest high of the current uptrend.

Acceleration Factor (AF): Starting at .02, AF increases by .02 each
time the extreme point makes a new high. AF can reach a maximum
of .20, no matter how long the uptrend extends.

Current SAR = Prior SAR + Prior AF(Prior EP - Prior SAR)
13-Apr-10 SAR = 48.28 = 48.13 + .14(49.20 - 48.13)

The Acceleration Factor is multiplied by the difference between the
Extreme Point and the prior period's SAR. This is then added to the
prior period's SAR. Note however that SAR can never be above the
prior two periods' lows. Should SAR be above one of those lows, use
the lowest of the two for SAR.

===

Falling SAR

Prior SAR: The SAR value for the previous period.

Extreme Point (EP): The lowest low of the current downtrend.

Acceleration Factor (AF): Starting at .02, AF increases by .02 each
time the extreme point makes a new low. AF can reach a maximum
of .20, no matter how long the downtrend extends.

Current SAR = Prior SAR - Prior AF(Prior SAR - Prior EP)
9-Feb-10 SAR = 43.56 = 43.84 - .16(43.84 - 42.07)

The Acceleration Factor is multiplied by the difference between the
Prior period's SAR and the Extreme Point. This is then subtracted
from the prior period's SAR. Note however that SAR can never be
below the prior two periods' highs. Should SAR be below one of
those highs, use the highest of the two for SAR.
'''
# high low
# bug, today's sar is wrong
def sar(prices):
    df = pd.DataFrame(prices.loc[:,['close', ]])
    #df = prices.loc[:,['close', 'high']] # <class 'pandas.core.series.Series'>
    #df = prices.loc[:,'close']
    #df = prices[:,['close', 'high']] # TypeError: unhashable type: 'slice'
    #df['sar'] = SAR(prices, timeperiod=4)
    df['sar'] = SAR(prices)
    #print(type(df)) # <class 'pandas.core.frame.DataFrame'>

    return df

# Directional Movement indicators
'''
Average Directional Index (ADX) measures trend strength without regard to trend direction.
Plus Directional Indicator (+DI) and Minus Directional Indicator (-DI), complement ADX by defining trend direction.

Directional movement is positive (plus) when the current high minus the prior high is greater than the prior low minus the current low. This so-called Plus Directional Movement (+DM) then equals the current high minus the prior high, provided it is positive. A negative value would simply be entered as zero.

Directional movement is negative (minus) when the prior low minus the current low is greater than the current high minus the prior high. This so-called Minus Directional Movement (-DM) equals the prior low minus the current low, provided it is positive. A negative value would simply be entered as zero.

1. Calculate the True Range (TR), Plus Directional Movement (+DM) and Minus Directional Movement (-DM) for each period.

2. Smooth these periodic values using the Wilder's smoothing techniques. These are explained in detail in the next section.

3. Divide the 14-day smoothed Plus Directional Movement (+DM) by the 14-day smoothed True Range to find the 14-day Plus Directional Indicator (+DI14). Multiply by 100 to move the decimal point two places. This +DI14 is the Plus Directional Indicator (green line) that is plotted along with ADX.

4. Divide the 14-day smoothed Minus Directional Movement (-DM) by the 14-day smoothed True Range to find the 14-day Minus Directional Indicator (-DI14). Multiply by 100 to move the decimal point two places. This -DI14 is the Minus Directional Indicator (red line) that is plotted along with ADX.

5. The Directional Movement Index (DX) equals the absolute value of +DI14 less - DI14 divided by the sum of +DI14 and - DI14.

6. After all these steps, it is time to calculate the Average Directional Index (ADX). The first ADX value is simply a 14-day average of DX. Subsequent ADX values are smoothed by multiplying the previous 14-day ADX value by 13, adding the most recent DX value and dividing this total by 14.
'''
'''
a strong trend is present when ADX is above 25 and no trend is present when below 20.
A buy signal occurs when ADX is above 20(25) and +DI crosses above -DI
A buy signal occurs when ADX is above 20(25) and -DI crosses above +DI
'''
# close high low
def dmi(prices):
    df = pd.DataFrame()
    df['pdi'] = PLUS_DI(prices, timeperiod=14)
    df['mdi'] = MINUS_DI(prices, timeperiod=14)
    df['adx'] = ADX(prices, timeperiod=14)
    df['adxr'] = ADXR(prices, timeperiod=14)

    return df

# Bollinger Bands
'''
Middle Band = 20-day simple moving average (SMA)
Upper Band = 20-day SMA + (20-day standard deviation of price x 2)
Lower Band = 20-day SMA - (20-day standard deviation of price x 2)
'''
'''
Signal: W-Bottoms
Signal: M-Tops
Signal: Walking the Bands

a move to the upper band shows strength, while a sharp move to the lower band shows weakness.
'''
# close
def bbands(prices):
    #upper, middle, lower = BBANDS(prices, timeperiod=20)#, matype=4)
    df = BBANDS(prices, timeperiod=20)#, matype=4) # upperband  middleband  lowerband

    return df

# Stochastic Oscillator
'''
%K = (Current Close - Lowest Low)/(Highest High - Lowest Low) * 100
%D = 3-day SMA of %K

Lowest Low = lowest low for the look-back period
Highest High = highest high for the look-back period
%K is multiplied by 100 to move the decimal point two places

Stochastic Oscillator is a momentum indicator that shows the location of the close relative to the high-low range over a set number of periods.

Stochastic Oscillator “doesn't follow price, it doesn't follow volume or anything like that. It follows the speed or the momentum of price. As a rule, the momentum changes direction before price.” As such, bullish and bearish divergences in the Stochastic Oscillator can be used to foreshadow reversals. This was the first, and most important, signal that Lane identified. Lane also used this oscillator to identify bull and bear set-ups to anticipate a future reversal. Because the Stochastic Oscillator is range bound, is also useful for identifying overbought and oversold levels.

===

The KDJ indicator is actually a derived form of the Stochastic with the only difference being an extra line called the J line.

The J line represents the divergence of the %D value from the %K. The value of J can go beyond [0, 100] for %K and %D lines on the chart.

%K = 100 * (Close-LowestLow[last n periods])/(HighestHigh[last n periods]-LowestLow[last n periods])
%D = MovingAverage(%K)
'''
# close high low
def kdj(prices):
    df = pd.DataFrame(prices.loc[:,'close'])

    # 9 3 3
    Hn = pd.rolling_max(prices['high'], 9)
    Ln = pd.rolling_min(prices['low'], 9)
    rsv = (prices['close'] - Ln)/(Hn - Ln) * 100

    df['k'] = pd.ewma(rsv, com=2)
    df['d'] = pd.ewma(df.k, com=2)
    df['j'] = 3*df.k - 2*df.d

    #k, d = STOCH(inputs, fastk_period=9, slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)
    #k, d = STOCH(inputs)
    #j = 3*k - 2*d

    return df

# Commodity Channel Index
# 顺势指标
'''
CCI = (Typical Price  -  20-period SMA of TP) / (.015 x Mean Deviation)

Typical Price (TP) = (High + Low + Close)/3

Constant = .015

MD = MA(|TP - MA(TP, N)|, N)

There are four steps to calculating the Mean Deviation.
First, subtract the most recent 20-period average of the typical price from each period's typical price.
Second, take the absolute values of these numbers.
Third, sum the absolute values.
Fourth, divide by the total number of periods (20).

CCI is a versatile indicator that can be used to identify a new trend or warn of extreme conditions.
CCI measures the current price level relative to an average price level over a given period of time.
CCI is relatively high when prices are far above their average.
CCI is relatively low when prices are far below their average.
CCI can be used to identify overbought and oversold levels.
'''
'''
CCI, 为极端行情而生
< -100: W/W+ 买点
> +100: M/M+ 卖点
'''
# close high low
def cci(prices):
    df = pd.DataFrame()
    df['cci'] = CCI(prices)

    return df

# Relative Strength Index
# 反映股价波动中 涨跌做的贡献
'''
              100
RSI = 100 - --------
             1 + RS

RS = Average Gain / Average Loss

The very first calculations for average gain and average loss are simple 14 period averages.

    First Average Gain = Sum of Gains over the past 14 periods / 14.
    First Average Loss = Sum of Losses over the past 14 periods / 14

The second, and subsequent, calculations are based on the prior averages and the current gain loss:

    Average Gain = [(previous Average Gain) x 13 + current Gain] / 14.
    Average Loss = [(previous Average Loss) x 13 + current Loss] / 14.

RSI calculation is based on 14 periods
RSI is considered overbought when above 70 and oversold when below 30
RSI tends to fluctuate between 40 and 90 in a bull market (uptrend) with the 40-50 zones acting as support.
RSI tends to fluctuate between 10 and 60 in a bear market (downtrend) with the 50-60 zone acting as resistance.
RSI is an extremely popular momentum indicator
'''
# close
def rsi(prices):
    df = pd.DataFrame()

    df['rsi_6'] = RSI(prices, timeperiod=6)
    df['rsi_12'] = RSI(prices, timeperiod=12)
    df['rsi_24'] = RSI(prices, timeperiod=24)

    #df['rsi_14'] = RSI(prices, timeperiod=14)

    return df

'''
乖离率（BIAS）是测量 [股价] 偏离 [均线(平均移动线)] 大小程度的指标。
乖离率=[(当日收盘价-N日平均价)/N日平均价]*100% 注, 平均价? 平均成本?
'''
def bias(prices):
    df = pd.DataFrame(prices.loc[:,'close'])
    #df['costs'] = pd.Series(prices['turnover']/prices['volume'])
    df['costs'] = prices['turnover']/prices['volume']

    ma1_6 = MA(df, timeperiod=6)
    ma1_12 = MA(df, timeperiod=12)
    ma1_24 = MA(df, timeperiod=24)
    df['bias1_6'] = (prices['close'] - ma1_6)/ma1_6 * 100
    df['bias1_12'] = (prices['close'] - ma1_12)/ma1_12 * 100
    df['bias1_24'] = (prices['close'] - ma1_24)/ma1_24 * 100

    return df

# close high low
# Average True Range
'''
ATR is an indicator that measures volatility.

Current ATR = [(Prior ATR x 13) + Current TR] / 14

  - Multiply the previous 14-day ATR by 13.
  - Add the most recent day's TR value.
  - Divide the total by 14

True Range (TR), which is defined as the greatest of the following:

    Method 1: Current High less the current Low
    Method 2: Current High less the previous Close (absolute value)
    Method 3: Current Low less the previous Close (absolute value)

If the current period's high is above the prior period's high and the low is below the prior period's low, then the current period's high-low range will be used as the True Range. This is an outside day that would use Method 1 to calculate the TR. This is pretty straight forward.
Methods 2 and 3 are used when there is a gap or an inside day.
A gap occurs when the previous close is greater than the current high (signaling a potential gap down or limit move) or the previous close is lower than the current low (signaling a potential gap up or limit move).
'''
def atr(prices):
    df = pd.DataFrame()
    df['atr'] = ATR(prices, timeperiod=14)

    return df
