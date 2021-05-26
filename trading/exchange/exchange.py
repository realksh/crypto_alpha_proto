import configparser
import ccxt

class ExchangeBinance(object):
    #이곳에 각 거래소 인스턴스를 만든다
    __instance = None

    def __init__(self):
        if ExchangeBinance.__instance:
            self.get_instance()

    @classmethod
    def get_instance(cls):
        if not cls.__instance:
            config = configparser.ConfigParser()
            config.read('conf/config.cfg')
            API_KEY = config['BINANCE']['apiKey']
            SECRET_KEY = config['BINANCE']['secretKey']
            cls.__instance = ccxt.binance(config={
                'apiKey': API_KEY,
                'secret': SECRET_KEY,
                'timeout': 30000,
                'enableRateLimit': True,
                'options': {
                    'defaultType': 'future',
                    'adjustForTimeDifference': True,
                },
            })
        return cls.__instance

b1 = ExchangeBinance.get_instance()
print(b1)
b2 = ExchangeBinance.get_instance()
print(b2)

print(b1 == b2)
