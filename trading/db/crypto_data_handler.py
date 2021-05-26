from datetime import date, datetime
import sys

from sqlalchemy.sql.sqltypes import Float
sys.path.append('.')
import sqlite3
import sqlalchemy
from trading.db.data_handler import DataHandler
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Candle(Base):
    __tablename__ = 'candles'

    timestamp = Column(datetime, primary_key=True)
    open = Column(String)
    high = Column(String)
    low = Column(String)
    close = Column(String)
    volume = Column(String)

    Index('timestamp_idx', 'timestamp')

    def __repr__(self):
        return "<Candle(timestamp='%s', open='%s', high='%s', low='%s', "\
                "close='%s', volume='%s')>" % (self.timestamp,
                    self.open, self.high, self.low,
                    self.close, self.volume)
class CryptoDataHandler(DataHandler):
    def __init__(self, symbol) -> None:

        sOhlcv = Ohlcv()
        file_name = symbol + '.db'
        self.conn = sqlite3.connect('test.db')

        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS 'crypto_ohlcvs' (
                symbol VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (symbol, date))
            """
            curs.execute(sql)

            self.conn.commit()
            self.codes = dict()
            
    def __del__(self):
        pass

    def insert_items(self, df):
        with self.conn.cursor() as curs:
            for r in df.itertuples():
                sql = f"REPLACE INTO min_price VALUES('{r.symbol}', "\
                    f"'{r.date}', {r.open}, {r.high}, {r.low}, {r.close}, "\
                    f"{r.volume})"
                curs.execute(sql)
            self.conn.commit()

    def find_items(self):
        pass
        

    def find_item(self):
        pass
   

    def delete_items(self):
        pass

    def update_items(self):
        pass

    def aggregate(self): 
        pass