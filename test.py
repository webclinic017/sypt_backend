import ccxt
import aips
import talib

exchange=ccxt.binance({
    'apiKey': aips.key,
    'secret': aips.secret,
    'enableRateLimit': True
})
print(exchange.fetch_balance()['USDT'])