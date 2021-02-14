import yfinance as yf

class Response():
    def __init__(self, option, res):
        self.option = option
        self.res = res


def getTicker(message):
    options = ['price', 'desc', 'high', 'low']
    split_string = message.split(' ')
    try:
        option = split_string[1]
        tick = split_string[2]
        if option not in options:
            raise Exception
        tick_info = (yf.Ticker(tick.upper())).info
        if option == 'price':
            res = {
                'ticker': tick,
                'price': tick_info.get('ask')
            }
            new_response = Response('price', res)
            print(new_response.res)
            return new_response
        elif option == 'desc':
            res = {
                'shortName': tick_info.get('shortName'),
                'sector': tick_info.get('sector'),
                'open': tick_info.get('open'),
                'dayLow': tick_info.get('dayLow'),
                'dayHigh': tick_info.get('dayHigh'),
                'website': tick_info.get('website')
            }
            new_response = Response('desc', res)
            return new_response
        elif option == 'high':
            res = {
                'ticker': tick,
                'dayHigh': tick_info.get('dayHigh')
            }
            new_response = Response('high', res)
            return new_response
        elif option == 'low':
            res = {
                'ticker': tick,
                'dayLow': tick_info.get('dayLow')
            }
            new_response = Response('low', res)
            return new_response
        else:
            raise Exception

    except Exception as e:
        print(e)
        return -1

def validateTickers(ticks):
    for tick in ticks:
        try:
            t = yf.Ticker(tick)
            t.actions
        except Exception as e:
            print(e)
            return False, tick
    return True, None

def getTickerPrice(tick):
    t = yf.Ticker(tick)
    return (t.info.get('ask')) 