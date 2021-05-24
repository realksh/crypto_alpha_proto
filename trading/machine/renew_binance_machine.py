import sys
sys.path.append('.')
import pyupbit
import pandas as pd
from tradingview_ta import TA_Handler, Interval, Exchange

df = pyupbit.get_ohlcv("KRW-BTC", "minute1", 500)
print(df)

df1 = df['open'].resample('15T').first()
df2 = df['high'].resample('15T').max()
df3 = df['low'].resample('15T').min()
df4 = df['close'].resample('15T').last()
df5 = df['volume'].resample('15T').sum()

df = pd.concat([df1, df2, df3, df4, df5], axis=1)
print(df)


btcusdt = TA_Handler(
    symbol="BTCUSDT",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_MINUTE
)
print(btcusdt.get_analysis().summary)

