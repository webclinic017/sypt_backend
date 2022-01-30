from ast import Param
import ccxt
import pandas as pd
import math
import time
import threading
import aips
import concurrent.futures

class binance():
    def exchange(KEY,SECRET):
        exchange = ccxt.binance({
            'apiKey': KEY,
            'secret': SECRET,
            'enableRateLimit': True
        })
        return exchange
    
    def ohlcv(symbol,KEY,SECRET):
        exchange=binance.exchange(KEY,SECRET)
        bars=exchange.fetch_ohlcv(symbol,timeframe = '1h',limit = 5)
        df=pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        lastindex=len(df.index)-1
        sellprice=df['low'][lastindex]*0.99
        buyprice=df['high'][lastindex]*1.05
        return buyprice,sellprice

    def PLACEORDER(symbol,KEY,SECRET):
        exchange=binance.exchange(KEY,SECRET)
        buy_amount=11
        position = False
        n=10
        for i in range(n*2):
            buyprice,sellprice=binance.ohlcv(symbol,KEY,SECRET)
            if not position :
                buy=exchange.create_order(symbol,'limit','buy',buy_amount,buyprice)
                while True:
                    balance=exchange.fetch_balance()['USDT']
                    usdt_used=balance['used']
                    if usdt_used==0:
                        break
                    else:
                        time.sleep(300) 
                        buyprice,sellprice=binance.ohlcv(symbol,KEY,SECRET)
                        if buyprice<float(buy['price']):
                            cancel=exchange.cancel_all_orders(symbol)
                            buy=exchange.create_order(symbol,'limit','buy',buy_amount,buyprice)
                        elif buyprice==float(buy['price']):
                            continue
                position = True
                buyID=int(buy['info']['orderId'])
                side="buy"
                print(buyID,side,position,buyprice)

            elif position:
                ada_balance=exchange.fetch_balance()['ADA']
                ada_free=float(ada_balance['free'])
                sell_amount=math.floor(ada_free)
                sell=exchange.create_order(symbol,'limit','sell',sell_amount,sellprice)
                sellID=int(sell['info']['orderId'])
                time.sleep(3600)
                while True:
                    buyprice,sellprice=binance.ohlcv(symbol,KEY,SECRET)
                    ada_balance=exchange.fetch_balance()['ADA']
                    ada_used=int(ada_balance['used'])
                    if ada_used==0:
                        break
                    else :
                        if sellprice>float(sell['price']):
                            #cancel order and place new order
                            cancel = exchange.cancel_all_orders(symbol)
                            cancelID=int(cancel['info']['orderId'])

                            side="cancel"
                            newsell=exchange.create_order(symbol,'limit','sell',sell_amount,sellprice)
                            # newsell=exchange.create_order(symbol,'stop_loss_limit','sell',sell_amount,sellprice,{'stopPrice':sellprice})
                            sellID=int(newsell['info']['orderId'])
                        time.sleep(3600)
                position = False
                side="sell"
                print(sellID,side,position,sellprice)
                        
threads = []
symbol = ['ADA/USDT','BTC/USDT','ETH/USDT']
i=0
for key,value in aips.api.items():
    print(key)
    for i in range(len(symbol)):
        t1 = threading.Thread(target=binance.PLACEORDER,args=(symbol[i],key,value))
        t1.start()
        threads.append(t1)
