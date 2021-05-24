import sys
from trading.db.crypto_data_handler import CryptoDataHandler
from trading.exchange.ohlcv_fetcher import OhlcvFetcher
sys.path.append('.')
import configparser
import pandas as pd
import ccxt
from trading.machine.base_machine import Machine
from trading.exchange.exchange import Exchange
from datetime import datetime, timezone

class BinanceMachine(Machine):

    TRADE_CURRENCY_TYPE = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'XRP/USDT']

    def __init__(self):
        self.binance = Exchange().binance

    def get_ticker(self, currency_type = None):
        """
        종목 정보 불러오기
        """
        if currency_type is None:
            raise Exception('Need to currency type')
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        
        ticker = self.binance.fetch_ticker(currency_type)
        ticker = self.binance.fetch_tickers()
        return ticker

    def get_tickers(self):
        """
        종목 리스트 정보 불러오기
        """
        tickers = self.binance.fetch_tickers()
        return tickers

    def get_ohlcvs(self, symbol, per = "14", since = None, limit = None):
        """
        List of filled orders
        """
        if symbol is None:
            raise Exception('Need to currency type')

        fetcher = OhlcvFetcher()
        fetcher.get_candles(symbol='ETH/USDT', debug=True)

        ohlcvs = self.binance.fetch_ohlcv(symbol, "1m", since, limit)

        for ohlc in ohlcvs:
            ohlc[0] = datetime.fromtimestamp(ohlc[0]/1000, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            ohlc.append(0)
            ohlc.append(0)

        df = pd.DataFrame(ohlcvs, columns=['index', 'open', 'high', 'low', 'close', 'volume', 'buy', 'sell'])
        df['index'] = pd.to_datetime(df['index'])
        df = df.set_index('index')
        print(df)

        return df

    def get_today_ohlcvs(self, symbol, per = "14"):
        if symbol is None:  
            raise Exception('Need to currency type')

        now = datetime.utcnow()
        today_str = now.strftime("%Y-%m-%d 00:00:00")
        
        ohlcvs = self.get_ohlcvs(symbol, per, self.binance.parse8601(today_str))

        open = ohlcvs['open'].resample(per + 'T').first()
        high = ohlcvs['high'].resample(per + 'T').max()
        low = ohlcvs['low'].resample(per + 'T').min()
        close = ohlcvs['close'].resample(per + 'T').last()
        volume = ohlcvs['volume'].resample(per + 'T').sum()         

        df = pd.concat([open, high, low, close, volume], axis=1)

        data_handler = CryptoDataHandler(symbol)
        
        return df

    def get_balance(self):
        balance = self.binance.fetch_balance()
        return balance

    def buy_future_market_order(self, currency_type, amount):
        """
        TODO
        스탑로스
        """
        order = self.binance.create_market_buy_order(currency_type, amount)
        return order

    def sell__future_market_order(self, currency_type, amount):
        """
        스탑로스 설정 필요
        """
        order = self.binance.create_market_sell_order(currency_type, amount)
        return order

    def cancel_order(self, order_id):
        """
        스탑로스 설정 필요
        """
        order = self.binance.cancel_order(order_id)
        return order