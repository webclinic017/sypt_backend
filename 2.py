import threading
from discord import Webhook, RequestsWebhookAdapter
import aips
class binance():
    def discord(key,value,symbol,side,price,timestamp,orderID):
        webhook_PERSONAL = Webhook.from_url("https://discord.com/api/webhooks/936517963543101440/L8FO04cxeL1xYKLE-n8P-voWJ8wJi3EJFpARcqEWydPTBiBT9wA9ZHg_O4qHhftixweN", adapter=RequestsWebhookAdapter())
        data=str(timestamp)+" "+str(orderID)+" "+str(symbol)+" "+str(side)+" "+str(price)
        webhook_PERSONAL.send(data)
    
    def PLACEORDER(symbol,KEY,VALUE):
        binance.discord(KEY,value,symbol,'buy',1.1,11,112)


threads = []
symbol = ['ADA/USDT','BTC/USDT','ETH/USDT']
i=0
for key,value in aips.api.items():
    print(key)
    for i in range(len(symbol)):
        t1 = threading.Thread(target=binance.PLACEORDER,args=(symbol[i],key,value))
        t1.start()
        threads.append(t1)
