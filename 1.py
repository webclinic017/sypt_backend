import ccxt 
import aips
exchange = ccxt.binance({
    'apiKey': aips.key,
    'secret': aips.sec,
    'enableRateLimit': True
})
symbol='ADA/USDT'
print(exchange.create_limit_buy_order(symbol,11,1))
print(exchange.fetch_balance()[symbol.split('/')[0]])
print(exchange.fetch_balance()[symbol.split('/')[1]])   
print(exchange.cancel_all_orders(symbol))