import sys
sys.path.append('.')
import pandas as pd
import ccxt.binance as binance
import ccxt
from trading.machine.base_machine import Machine
from datetime import datetime
from abc import ABC

class TBBT(ABC):
    def __init__(self) -> None:
        super().__init__()

    def process_tbbt(self, ohlcvs):
        if len(ohlcvs) < 4:
            pass

        now = ohlcvs[-2]
        before_one = ohlcvs[-3]
        before_two = ohlcvs[-4]

        upper = 0
        lower = 0

        if now['high'] > before_one['high']:
            upper = upper + 1
            if before_one['high'] > before_two['high']:
                upper = upper + 1
        
        if now['low'] > before_one['low']:
            upper = upper + 1
            if before_one['low'] > before_two['low']:
                upper = upper + 1

