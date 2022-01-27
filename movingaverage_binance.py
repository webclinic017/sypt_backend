from ast import Param
import ccxt
import pandas as pd
import API
import numpy as np
import math
import time
import csv
import threading
import aips
import concurrent.futures


symbol = 'ADA/USDT'
class binance():
    def exchange(KEY,SECRET):
        exchange = ccxt.binance({
            'apiKey': KEY,
            'secret': SECRET,
            'enableRatemarket': True
        })
        return exchange
    
    def ohlcv(KEY,SECRET):
        exchange=binance.exchange(KEY,SECRET)
        bars=exchange.fetch_ohlcv(symbol,timeframe = '1h',limit = 21)
        df=pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df=df['close']
        lastindex=len(df.index)-1
        a=np.array(df)
        movingaverage= np.mean(a, axis = 0) 
        while True:
            if df[lastindex]>movingaverage:
                return True
            else :
                return False

    def PLACEORDER(KEY,SECRET):
        exchange=binance.exchange(KEY,SECRET)
        buy_amount=11
        position = False
        n=1
        for _ in range(n*2):
            ohlc=binance.ohlcv(KEY,SECRET)
            if not position and ohlc:
                buy=exchange.create_market_buy_order(symbol,buy_amount)
                while True:
                    balance=exchange.fetch_balance()['USDT']
                    usdt_used=balance['used']
                    if usdt_used==0:
                        break
                    else:
                        continue
                position = True
                buyID=int(buy['info']['orderId'])
                side="buy"
                print(buyID,side,position,KEY)
                while True:
                    if not ohlc:
                        break
                    else:
                        ohlc=binance.ohlcv(KEY,SECRET)
                        time.sleep(100)

            elif position and not ohlc:
                ada_balance=exchange.fetch_balance()['ADA']
                ada_free=float(ada_balance['free'])
                sell_amount=math.floor(ada_free)
                sell=exchange.create_market_sell_order(symbol,sell_amount)
                sellID=int(sell['info']['orderId'])
                time.sleep(3600)
                while True:
                    ada_balance=exchange.fetch_balance()['ADA']
                    ada_used=int(ada_balance['used'])
                    if ada_used==0:
                        break
                    else :
                        time.sleep(60)
                position = False
                side="sell"
                print(sellID,side,position,KEY)
threads = []
for key,value in aips.api.items():
    t1 = threading.Thread(target=binance.PLACEORDER,args=(key,value))
    t1.start()
    threads.append(t1)