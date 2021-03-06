from ast import Param
import ccxt
import pandas as pd
import math
import time
import threading
import aips
import concurrent.futures
from discord import Webhook, RequestsWebhookAdapter

class binance():
    def discord(key,value,symbol,side,price,timestamp,orderID):
        webhook_PERSONAL = Webhook.from_url("https://discord.com/api/webhooks/936517963543101440/L8FO04cxeL1xYKLE-n8P-voWJ8wJi3EJFpARcqEWydPTBiBT9wA9ZHg_O4qHhftixweN", adapter=RequestsWebhookAdapter())
        data=str(timestamp)+" "+str(orderID)+" "+str(symbol)+" "+str(side)+" "+str(price)
        webhook_PERSONAL.send(data)
    def exchange(KEY,SECRET):
        exchange = ccxt.binance({
            'apiKey': KEY,
            'secret': SECRET,
            'enableRateLimit': True
        })
        return exchange
    
    def ohlcv(symbol,KEY,SECRET):
        usdt_amount=11
        exchange=binance.exchange(KEY,SECRET)
        bars=exchange.fetch_ohlcv(symbol,timeframe='1h',limit=5)
        df=pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        lastindex=len(df.index)-1
        # sellprice=float(df['high'][lastindex])*1.05
        # buyprice=float(df['low'][lastindex])*0.99
        sellprice=float(df['high'][lastindex])
        buyprice=float(df['low'][lastindex])
        close=float(df['close'][lastindex])
        symbol_amount=float(usdt_amount/close)
        return buyprice,sellprice,symbol_amount

    def PLACEORDER(symbol,KEY,SECRET):
        time.sleep(5)
        exchange=binance.exchange(KEY,SECRET)
        position = False
        n=5
        for i in range(n*2):
            buyprice,sellprice,symbol_amount=binance.ohlcv(symbol,KEY,SECRET)
            if not position :
                buy=exchange.create_limit_buy_order(symbol,symbol_amount,buyprice)
                while True:
                    filled=float(buy['filled'])
                    if filled!=0:
                        break
                    else:
                        buyprice,sellprice,symbol_amount=binance.ohlcv(symbol,KEY,SECRET)
                        if buyprice<float(buy['price']):
                            cancel=exchange.cancel_all_orders(symbol)
                            buy=exchange.create_limit_buy_order(symbol,symbol_amount,buyprice)
                        elif buyprice==float(buy['price']):
                            continue
                        time.sleep(300) 
                position = True
                buyID=int(buy['info']['orderId'])
                side="buy"
                print(buyID,side,position,buyprice)
                timestamp=buy['timestamp']
                binance.discord(KEY,SECRET,symbol,side,buyprice,timestamp,buyID)

            elif position:
                symbol_balance=exchange.fetch_balance()[symbol.split('/')[0]]
                # symbol_free=float(symbol_balance['free'])
                # sell_amount=math.floor(symbol_free)
                sell_amount=symbol_balance['free']
                sell=exchange.create_limit_sell_order(symbol,sell_amount,sellprice)
                sellID=int(sell['info']['orderId'])
                time.sleep(3600)
                while True:
                    buyprice,sellprice,symbol_amount=binance.ohlcv(symbol,KEY,SECRET)
                    symbol_balance=exchange.fetch_balance()[symbol.split('/')[0]]
                    symbol_used=int(symbol_balance['used'])
                    if symbol_used==0:
                        break
                    else :
                        if sellprice>float(sell['price']):
                            cancel = exchange.cancel_all_orders(symbol)
                            cancelID=int(cancel['info']['orderId'])
                            side="cancel"
                            newsell=exchange.create_limit_sell_order(symbol,sell_amount,sellprice)
                            sellID=int(newsell['info']['orderId'])
                        time.sleep(3600)
                position = False
                side="sell"
                timestamp=sell['timestamp']
                binance.discord(KEY,SECRET,symbol,side,sellprice,timestamp,sellID)
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
