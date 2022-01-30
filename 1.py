import ccxt
import aips

exchange=ccxt.binance({
    'apiKey': aips.key,
    'secret': aips.sec,
    'enableRateLimit': True
})

print(exchange.fetch_balance()['USDT'])
# print(exchange.fetch_my_trades('ETH'))