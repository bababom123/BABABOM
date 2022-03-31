import upbit_privat_api as upa
import select_coin as sc
import pyupbit
import datetime
import time

with open("upbit_openapikey.txt") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    upbit = pyupbit.Upbit(key, secret)


tickers = ['KRW-BTC', 'KRW-ETH', 'KRW-BCH', 'KRW-AAVE', 'KRW-LTC', 'KRW-SOL', 'KRW-BSV', 'KRW-AVAX', 'KRW-AXS', 'KRW-WAVES', 'KRW-ETC', 'KRW-BTG', 'KRW-STRK', 'KRW-ATOM', 'KRW-NEO', 'KRW-DOT', 'KRW-LINK', 'KRW-REP', 'KRW-NEAR', 'KRW-QTUM']
# tickers = list(sc.get_Top_MarketGap_n(50)['ticker'])

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1) # 자정

while True:
    try:
        for ticker in tickers:
            now = datetime.datetime.now()
            target_price = upa.get_target_price(ticker)
            ma5 = upa.get_yesterday_ma_n(ticker, 5) 

            if mid < now < mid + datetime.timedelta(second=10): # 코드의 실행 속도 때문에 정확한 시간 비교는 불가능하므로 범위를 통해 유추한다.
                now = datetime.datetime.now()
                mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
                ma5 = upa.get_yesterday_ma_n(ticker, 5)
                print(ticker, "매도발생")
                upa.sell_crypto_currency(ticker)
            
            if(upa.KRW <= 1): # 원화 없으면 매수 안함
                continue        

            current_price = pyupbit.get_current_price(ticker)
            if (current_price > target_price) and (current_price > ma5):
                print(ticker, "매수발생")
                upa.buy_crypto_currency(ticker)
            time.sleep(0.3)
        # print("whee...")
    except:
        print("에러 발생")
        exit(1)    
