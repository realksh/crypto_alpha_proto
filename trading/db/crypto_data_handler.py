import sys
sys.path.append('.')
import sqlite3
from trading.db.data_handler import DataHandler

class CryptoDataHandler(DataHandler):

    def __init__(self, symbol) -> None:

        file_name = './' + symbol + '.db'
        self.conn = sqlite3.connect(file_name)

        with self.conn.cursor() as curs:
            sql = """
            CREATE TABLE IF NOT EXISTS crypto_info (
                code VARCHAR(20),
                date DATE,
                open BIGINT(20),
                high BIGINT(20),
                low BIGINT(20),
                close BIGINT(20),
                volume BIGINT(20),
                PRIMARY KEY (code, date))
            """
            curs.execute(sql)

            self.conn.commit()
            self.codes = dict()
            
    def __del__(self):
        self.conn.close()

    def insert_items(self, df):
        with self.conn.cursor() as curs:
            for r in dg.itertuples():
                sql = f"REPLACE INTO min_price VALUES('{code}', "\
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