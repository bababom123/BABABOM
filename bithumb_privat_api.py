import pybithumb
import time
import datetime

# con_key = "97dd8f3576d7e5b15dabe249acc7f0fe"
# sec_key = "05b4e649b771e3d50536357aa8c17771"

# bithumb = pybithumb.Bithumb(con_key, sec_key)

with open("bithumb.txt") as f:
    lines = f.readlines()
    key = lines[0].strip()
    secret = lines[1].strip()
    bithumb = pybithumb.Bithumb(key, secret)

# # 잔고 확인
# for ticker in pybithumb.get_tickers():
#     balance = bithumb.get_balance(ticker)
#     print(ticker, ": ", balance)
#     time.sleep(0.1)

# 매수
# 지정가 매수는 buy_limit_order(ticker, price, quantity)

# 변동성 돌파 전략 구현하기
def get_target_price(ticker):
    df = pybithumb.get_ohlcv(ticker) # 시가, 고가, 저가, 종가, 거래량
    yesterday = df.iloc[-2] 

    today_open = yesterday['close']
    yesterday_high = yesterday['high']
    yesterday_low = yesterday['low']
    target = (yesterday_high - yesterday_low) * 0.5 + today_open
    return target

def buy_crypto_currency(ticker):
    krw = bithumb.get_balance(ticker)[2] # 원화 보유액
    orderbook = pybithumb.get_orderbook(ticker) # ticker의 호가 정보
    sell_price = orderbook['asks'][0]['price'] # 호가 정보 중 매도호가 중 젤 작은거 중 가격
    unit = krw/float(sell_price) # 최우선 매도호가로 살 수 있는 개수
    bithumb.buy_market_order(ticker, unit) # 매수

def sell_crypto_currency(ticker):
    unit = bithumb.get_balance(ticker)[0] # ticker 보유 개수
    bithumb.sell_market_order(ticker, unit) # 매도

def get_yesterday_ma5(ticker):
    df = pybithumb.get_ohlcv(ticker)
    close = df['close']
    ma5 = close.rolling(window=5).mean()
    return ma5[-2]

now = datetime.datetime.now()
mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
target_price = get_target_price("BTC")
ma5 = get_yesterday_ma5("BTC")


while True:
    try:
        now = datetime.datetime.now()
        if mid < now < mid + datetime.timedelta(second=10): # 코드의 실행 속도 때문에 정확한 시간 비교는 불가능하므로 범위를 통해 유추한다.
            now = datetime.datetime.now()
            mid = datetime.datetime(now.year, now.month, now.day) + datetime.timedelta(1)
            ma5 = get_yesterday_ma5("BTC")
            print("매도발생")
            sell_crypto_currency("BTC")
        
        current_price = pybithumb.get_current_price("BTC")
        if (current_price > target_price) and (current_price > ma5):
            print("매수발생")
            buy_crypto_currency("BTC")
            
    except:
        print("에러 발생")
    
    time.sleep(1)

