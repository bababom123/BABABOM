import pyupbit
import datetime
import time

# with open("upbit_openapikey.txt") as f:
#     lines = f.readlines()
#     key = lines[0].strip()
#     secret = lines[1].strip()
#     upbit = pyupbit.Upbit(key, secret)

upbit = pyupbit.Upbit("wk4aLyOF6apllUZqRZQS3iRxvxoPPzC9OVLl6KLY", "Fg5qbayqsq2dTxyeYCkpJZ3M7xBf2nLx0XoatSMj")

KRW = upbit.get_balance("KRW") # 원화 보유액

def get_target_price(ticker):
    df = pyupbit.get_ohlcv(ticker) # 시가, 고가, 저가, 종가, 거래량
    yesterday = df.iloc[-2] 
    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = (yesterday_high - yesterday_low) * 0.7 + today_open
    return target

def buy_crypto_currency(ticker):
    orderbook = pyupbit.get_orderbook(ticker) # ticker의 호가 정보
    sell_price = orderbook['orderbook_units'][0]['ask_price'] # 매도호가 중 젤 작은거 중 가격
    vol = KRW/float(sell_price) * 0.9995 # 최우선 매도호가로 살 수 있는 가격
    upbit.buy_limit_order(ticker, sell_price, vol) # 매수

def sell_crypto_currency(ticker):
    vol = upbit.get_balance(ticker) # ticker 보유 개수
    upbit.sell_market_order(ticker, vol) # 매도

def get_yesterday_ma_n(ticker, n):
    df = pyupbit.get_ohlcv(ticker)
    close = df['close']
    ma_n = close.rolling(window=n).mean()
    return ma_n[-2]

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

tickers = ['KRW-BTC', 'KRW-ETH', 'KRW-BCH', 'KRW-AAVE', 'KRW-LTC', 'KRW-SOL', 'KRW-BSV', 'KRW-AVAX', 'KRW-AXS', 'KRW-WAVES', 'KRW-ETC', 'KRW-BTG', 'KRW-STRK', 'KRW-ATOM', 'KRW-NEO', 'KRW-DOT', 'KRW-LINK', 'KRW-REP', 'KRW-NEAR', 'KRW-QTUM']
# tickers = list(sc.get_Top_MarketGap_n(50)['ticker'])

now = datetime.datetime.now()
Basket = []

print("start")
while True:
    try:
        now = datetime.datetime.now()
        end_time = get_start_time(ticker) + datetime.timedelta(days=1) # 다음날 9시

        if not Basket: # 산 코인이 없다면
            for ticker in tickers:               
                target_price = get_target_price(ticker)
                ma5 = get_yesterday_ma_n(ticker, 5)                 
                if(KRW <= 1): # 원화 없으면 매수 안함
                    continue        
                current_price = pyupbit.get_current_price(ticker)
                if (current_price > target_price) and (current_price > ma5):
                    buy_crypto_currency(ticker)
                    Basket.append(ticker)
                    print(ticker, " BUY")
                time.sleep(0.3)            
        else:
            ticker = Basket[0]           
            if end_time - datetime.timedelta(second=5) < now < end_time: # 코드의 실행 속도 때문에 정확한 시간 비교는 불가능하므로 범위를 통해 유추한다.
                now = datetime.datetime.now()
                ma5 = get_yesterday_ma_n(ticker, 5)
                sell_crypto_currency(ticker)
                Basket.pop()
                print(ticker, " SELL")
            time.sleep(0.3)
        
    except:
        print("ERR")
        time.sleep(1)
