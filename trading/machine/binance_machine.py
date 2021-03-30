import sys
sys.path.append('.')
import configparser
import asyncio
import pandas as pd
import ccxt
from ccxt.binance import binance

from trading.machine.base_machine import Machine

class BinanceMachine(Machine):

    TRADE_CURRENCY_TYPE = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'XRP/USDT']

    def __init__(self):
        """
        config.ini 에서 api 관련 key 를 읽어 온다.
        """

        config = configparser.ConfigParser()
        config.read('conf/config.cfg')

        self.API_KEY = config['BINANCE']['apiKey']
        self.SECRET_KEY = config['BINANCE']['secretKey']
        self.binance = ccxt.binance(config={
            'apiKey' : self.API_KEY,
            'secret' : self.SECRET_KEY,
            'timeout': 30000,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',
                'adjustForTimeDifference': True,
            },
        })

    def get_ticker(self, currency_type = None):
        """
        종목 정보 불러오기
        """
        if currency_type is None:
            raise Exception('Need to currency type')
        if currency_type not in self.TRADE_CURRENCY_TYPE:
            raise Exception('Not support currency type')
        
        ticker = binance().fetch_ticker(currency_type)
      
        return ticker

    def get_ohlcvs(self, currency_type, per = '1m'):
        """
        List of filled orders
        """

        if currency_type is None:
            raise Exception('Need to currency type')
        
        ohlcv = binance().fetch_ohlcv(currency_type, per)

        df = pd.DataFrame(ohlcv, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
        df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
        
        return df

    def get_balance(self):
        balance = self.binance.fetch_balance()
        return balance

    def buy_market_order(self, currency_type, amount):
        """
        스탑로스 설정 필요
        """
        order = self.binance.create_market_buy_order(currency_type, amount)
        return order

    def sell_market_order(self, currency_type, amount):
        """
        스탑로스 설정 필요
        """
        order = self.binance.create_market_sell_order(currency_type, amount)
        return order

    def cancel_order(self, currency_type, amount):
        """
        스탑로스 설정 필요
        """
        order = self.binance.create_market_sell_order(currency_type, amount)
        return order