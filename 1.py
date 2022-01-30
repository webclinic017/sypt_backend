import ccxt
import aips
import pandas as pd
exchange=ccxt.binance({
    'apiKey': aips.key,
    'secret': aips.sec,
    'enableRateLimit': True
})

print(exchange.fetch_balance()['USDT'])
usdt_amount=11
symbol='BTC/USDT'


# print(ohlcv('BTC/USDT'))
# print(exchange.fetch_balance()['USDT'])
# print(exchange.fetch_my_trades('ETH'))
# print(exchange.cancel_all_orders('BTC'))
# print(exchange.cancel_all_orders('ETH'))
# print(exchange.cancel_all_orders('ADA/USDT'))
# print(exchange.fetch_open_orders('ADA/USDT'))
import threading
class binance():
    def PLACEORDER(symbol,KEY,VALUE):
        print(exchange.fetch_balance()[symbol.split('/')[1]])
        # print(symbol)

threads = []
symbol = ['ADA/USDT','BTC/USDT','ETH/USDT']
i=0
for key,value in aips.api.items():
    def ohlcv(symbol):
        bars=exchange.fetch_ohlcv(symbol,timeframe='5m',limit=5)
        df=pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        lastindex=len(df.index)-1
        buyprice=float(df['low'][lastindex])*0.98
        sellprice=float(df['high'][lastindex])*1.05
        close=float(df['close'][lastindex])
        symbol_amount=float(close/usdt_amount)
        return buyprice,sellprice,symbol_amount
    print(key)
    for i in range(len(symbol)):
        t1 = threading.Thread(target=binance.PLACEORDER,args=(symbol[i],key,value))
        t1.start()
        threads.append(t1)