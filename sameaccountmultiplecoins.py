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
    def discord(symbol,side,price,timestamp,orderID):
        webhook_PERSONAL = Webhook.from_url("https://discord.com/api/webhooks/936517963543101440/L8FO04cxeL1xYKLE-n8P-voWJ8wJi3EJFpARcqEWydPTBiBT9wA9ZHg_O4qHhftixweN", adapter=RequestsWebhookAdapter())
        data=str(timestamp)+" "+str(orderID)+" "+str(symbol)+" "+str(side)+" "+str(price)
        webhook_PERSONAL.send(data)
    def exchange():
        exchange = ccxt.binance({
            'apiKey': aips.key,
    'secret': aips.sec,
    'enableRateLimit': True
        })
        return exchange
    
    def ohlcv(symbol):
        exchange=binance.exchange()
        bars=exchange.fetch_ohlcv(symbol,timeframe = '5m',limit = 5)
        df=pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        lastindex=len(df.index)-1
        sellprice=float(df['high'][lastindex])*1.05
        buyprice=float(df['low'][lastindex])*0.98
        return buyprice,sellprice

    def PLACEORDER(symbol):
        print(symbol)
        exchange=binance.exchange()
        buy_amount=11
        position = False
        n=5
        for i in range(n*2):
            buyprice,sellprice=binance.ohlcv(symbol)
            if not position :
                buy=exchange.create_limit_buy_order(symbol,buy_amount,buyprice)
                while True:
                    balance=exchange.fetch_balance()['USDT']
                    usdt_used=balance['used']
                    if usdt_used==0:
                        break
                    else:
                        time.sleep(60) 
                        buyprice,sellprice=binance.ohlcv(symbol)
                        if buyprice<float(buy['price']):
                            buyIDtocancel=int(buy['info']['orderId'])
                            cancel=exchange.cancel_order(buyIDtocancel,symbol)
                            buy=exchange.create_limit_buy_order(symbol,buy_amount,buyprice)
                        elif buyprice==float(buy['price']):
                            continue
                position = True
                buyID=int(buy['info']['orderId'])
                side="buy"
                print(buyID,side,position,buyprice)
                timestamp=buy['timestamp']
                binance.discord(symbol,side,buyprice,timestamp,buyID)

            elif position:
                ada_balance=exchange.fetch_balance()['ADA']
                ada_free=float(ada_balance['free'])
                sell_amount=math.floor(ada_free)
                sell=exchange.create_limit_sell_order(symbol,sell_amount,sellprice)
                sellID=int(sell['info']['orderId'])
                time.sleep(300)
                while True:
                    buyprice,sellprice=binance.ohlcv(symbol)
                    ada_balance=exchange.fetch_balance()['ADA']
                    ada_used=int(ada_balance['used'])
                    if ada_used==0:
                        break
                    # else :
                    #     if sellprice>float(sell['price']):
                    #         #cancel order and place new order
                    #         cancel = exchange.cancel_all_orders(symbol)
                    #         cancelID=int(cancel['info']['orderId'])
                    #         side="cancel"
                    #         newsell=exchange.create_order(symbol,'limit','sell',sell_amount,sellprice)
                    #         # newsell=exchange.create_order(symbol,'stop_loss_limit','sell',sell_amount,sellprice,{'stopPrice':sellprice})
                    #         sellID=int(newsell['info']['orderId'])
                    #     time.sleep(300)
                position = False
                side="sell"
                timestamp=sell['timestamp']
                binance.discord(symbol,side,sellprice,timestamp,sellID)
                print(sellID,side,position,sellprice)
                        
threads = []
symbol = ['ADA/USDT','BTC/USDT','ETH/USDT']
i=0
for i in range(len(symbol)):
    t1 = threading.Thread(target=binance.PLACEORDER,args=(symbol[i]))
    t1.start()
    threads.append(t1)
