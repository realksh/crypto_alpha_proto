import sys
from time import sleep, strftime, time

from pandas._libs.tslibs import Timestamp
sys.path.append('.')
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
import time
import os
import re
from trading.exchange.exchange import ExchangeBinance
from trading.machine.base_machine import Machine
import pandas as pd
from pprint import pprint

class BinanceMachine(Machine):

    TRADE_CURRENCY_TYPE = ['BTC/USDT', 'ETH/USDT',
                           'BNB/USDT', 'ADA/USDT', 'XRP/USDT']




    def __init__(self):
        self.binance = ExchangeBinance.get_instance()

    def get_ticker(self, currency_type=None):
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

    def get_candles(self, symbol, timeframe="14m"):
        if symbol is None:
            raise Exception('Need to currency type')

        ohlcvs_1m = self.__get_ohlcvs(symbol)
        df = self.resample_timeframe(ohlcvs_1m, timeframe)

        pprint(df)
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


    def message(message, header="Error"):
        print(header.center(80, '-'))
        print(message)
        print('-'*80)


    def last_candle_is_incomplete(self, candle_timestamp, candle_timeframe):
        timeframe_re = re.compile(r'(?P<number>\d+)(?P<unit>[smhdwMy]{1})')
        match = timeframe_re.match(candle_timeframe)
        seconds = minutes = hours = days = weeks = months = years = 0
        lookup_dict = {'s': seconds, 'm': minutes, 'h': hours, 'd': days, 'w': weeks,
            'M': months, 'y': years}\

        if match is not None:
            matchdict = match.groupdict()
            lookup_dict[matchdict['unit']] = int(matchdict['number'])
            candle_dt = datetime.fromtimestamp(candle_timestamp / 1000)
            exchange_dt = datetime.fromtimestamp(self.binance.milliseconds() / 1000)
            # eg. timeframe=1d and candle_timestamp=2019-01-01T00:00:00Z
            #  exchange_dt=2019-01-02T01:00:00Z
            #
            #  2019-01-02T01:00:00Z - 1 day = 2019-01-01T00:00:00Z
            # use relativetimedelta as included batteries don't offer years
            #  or months
            one_candle_delta = relativedelta(years=lookup_dict['y'],
                months=lookup_dict['M'], weeks=lookup_dict['w'],
                days=lookup_dict['d'], hours=lookup_dict['h'],
                minutes=lookup_dict['m'], seconds=lookup_dict['s'])
            return exchange_dt - one_candle_delta < candle_dt

        else:
            self.message("Could not parse timeframe %s" % candle_timeframe, header="Error")

    def __get_ohlcvs(self, symbol):
        """
        List of filled orders
        """
        if symbol is None:
            raise Exception('Need to currency type')

        timeframe = '1m'
        now = datetime.now(timezone.utc)
        since = now.replace(hour=0, minute=0, second=0)
        since_timestamp = int(since.timestamp()) * 1000
        ohlcvs = None

        while True:
            time.sleep(0.2)
            ohlcv_batch = self.binance.fetch_ohlcv(symbol, timeframe, self.binance.parse8601(self.binance.iso8601(since_timestamp)))
            if ohlcv_batch and len(ohlcv_batch):
                last_candle = ohlcv_batch[-1]
                last_candle_timestamp = since_timestamp = last_candle[0]

                if self.last_candle_is_incomplete(last_candle_timestamp, timeframe):
                    del ohlcv_batch[-1]
                    if not ohlcv_batch:
                        break

                if ohlcvs is None:
                    ohlcvs = ohlcv_batch
                else:
                    for obj in ohlcv_batch:
                        if ohlcvs[-1][0] < obj[0]:
                            ohlcvs.append(obj)

        """
        for ohlc in ohlcvs:
            ohlc[0] = datetime.fromtimestamp(
            ohlc[0]/1000, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        ohlc.append(0)
        ohlc.append(0)
        """

        df = pd.DataFrame(ohlcvs, columns=[
                          'timestamp', 'open', 'high', 'low', 'close', 'volume'])
        # df['timestamp'] = pd.to_datetime(df['timestamp'])
        # df['datetime'] = datetime.fromtimestamp(
        #     df['timestamp']/1000, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

        # df = pd.DataFrame(ohlcvs, columns=[
        #                   'timestamp', 'open', 'high', 'low', 'close', 'volume', 'buy', 'sell'])
        # df['datetime'] = pd.to_datetime(df['timestamp'])
        df['datetime'] = df['timestamp'].apply(self.timestamp_to_datetime)
        df['datetime'] = pd.to_datetime(df['datetime'])
        df = df.set_index('datetime')

        return df

    def timestamp_to_datetime(self, timestamp):
        return datetime.fromtimestamp(timestamp/1000, timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        
    def resample_timeframe(self, ohlcvs, timeframe):
        per = timeframe[:-1]
        timestamp = ohlcvs['timestamp'].resample(per + 'T').first()
        open = ohlcvs['open'].resample(per + 'T').first()
        high = ohlcvs['high'].resample(per + 'T').max()
        low = ohlcvs['low'].resample(per + 'T').min()
        close = ohlcvs['close'].resample(per + 'T').last()
        volume = ohlcvs['volume'].resample(per + 'T').sum()

        df = pd.concat([timestamp, open, high, low, close, volume], axis=1)
        df['buy_signal'] = 0
        df['sell_signal'] = 0

        last = df.tail(1)
        last_candle_timestamp = last.values[0][0]

        if self.last_candle_is_incomplete(last_candle_timestamp, timeframe):
            df = df[:-1]
            
        return df

b = BinanceMachine()
obj = b.get_candles('ETH/USDT')
pprint(obj)