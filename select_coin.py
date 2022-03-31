import pyupbit
import time
from pandas import DataFrame, Series

def get_Top_MarketGap_n(n):
    df = {}
    tickers = pyupbit.get_tickers(fiat="KRW")

    for ticker in tickers:
        df[ticker] = pyupbit.get_current_price(ticker)
        time.sleep(0.1)

    df = sorted(df.items(), key=lambda x: x[1], reverse=True)
    ret = df[:n]
    columns = ["ticker", "current_price"]
    TMG = DataFrame(data=ret, columns=columns)

    return TMG


# dat = pyupbit.get_ohlcv('KRW-BTC')
# print(dat)
    
# print(list(get_Top_MarketGap_n(20)['ticker']))

# 22-03-30
# ['KRW-BTC', 'KRW-ETH', 'KRW-BCH', 'KRW-AAVE', 'KRW-LTC', 'KRW-SOL', 'KRW-BSV', 'KRW-AVAX', 'KRW-AXS', 'KRW-WAVES', 'KRW-ETC', 'KRW-BTG',
#  'KRW-STRK', 'KRW-ATOM', 'KRW-NEO', 'KRW-DOT', 'KRW-LINK', 'KRW-REP', 'KRW-NEAR', 'KRW-QTUM']

#        ticker  current_price
# 0     KRW-BTC     56869000.0
# 1     KRW-ETH      4090000.0
# 2     KRW-BCH       457100.0
# 3    KRW-AAVE       281550.0
# 4     KRW-LTC       158250.0
# 5     KRW-SOL       136450.0
# 6     KRW-BSV       119600.0
# 7    KRW-AVAX       112000.0
# 8     KRW-AXS        78280.0
# 9   KRW-WAVES        63510.0
# 10    KRW-ETC        60020.0
# 11    KRW-BTG        53190.0
# 12   KRW-STRK        51430.0
# 13   KRW-ATOM        36230.0
# 14    KRW-NEO        34970.0
# 15    KRW-DOT        26850.0
# 16   KRW-LINK        20800.0
# 17    KRW-REP        19530.0
# 18   KRW-NEAR        17000.0
# 19   KRW-QTUM        11290.0