import unittest
import sys
sys.path.append(".")
from trading.machine.binance_machine import BinanceMachine
import inspect
from pprint import pprint

class BinanceMachineTestCase(unittest.TestCase):

    def setUp(self):
        self.binance_machine = BinanceMachine()

    def test_get_ticker(self):
        print(inspect.stack()[0][3])
        ticker = self.binance_machine.get_ticker("ETH/USDT")
        assert ticker
        print(ticker)
        
    def test_get_ohlcvs(self):
        print(inspect.stack()[0][3])
        ohlcvs = self.binance_machine.get_candles("ETH/USDT", '14m')
        assert not ohlcvs.empty
        pprint(ohlcvs)

    def test_get_balance(self):
        print(inspect.stack()[0][3])
        balance = self.binance_machine.get_balance()
        assert balance
        print(balance['USDT'])

    def tearDown(self):
        pass
