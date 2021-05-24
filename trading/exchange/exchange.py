import configparser
import ccxt

class Exchange(object):
    #이곳에 각 거래소 인스턴스를 만든다
    __binance = None
    __upbit = None

    def __init__(self):
        pass

    @property
    def binance(self):
        if not self.__binance:
            config = configparser.ConfigParser()
            config.read('conf/config.cfg')
            API_KEY = config['BINANCE']['apiKey']
            SECRET_KEY = config['BINANCE']['secretKey']
            self.__binance = ccxt.binance(config={
            'apiKey' : API_KEY,
            'secret' : SECRET_KEY,
            'timeout': 30000,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'future',
                'adjustForTimeDifference': True,
            },
        })
        
        return self.__binance

b1 = Exchange.binance
print(b1)
b2 = Exchange.binance
print(b2)

print(b1 == b2)