# Binance API
from binance import Client
api_key = 'CSEUGkub6mSk4HrqUMc3M16gmnIDA9ENZgN0INKzgolqTURxZZ7bfaMCgyBFo10I'
api_secret = 'UMcmk6M0LwNntRBtE8n6VHW8B9Wk7dcKcLAP6BJjOGt7iiUZcYFN4mgI2hlVCHdy'
client = Client(api_key, api_secret)
client.API_URL = 'https://testnet.binance.vision/api'

# Get Data from Binance API
btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
ltc_price = client.get_symbol_ticker(symbol="LTCUSDT")
btc_tick = client.get_ticker(symbol="BTCUSDT")
ltc_tick = client.get_ticker(symbol="LTCUSDT")

# price_change_btc price_change_eth coin_to_mine
# up down btc
# up up btc
# down up ltc
# down down ltc

# Get current prices, for inference
def get_prices():
    api_key = 'CSEUGkub6mSk4HrqUMc3M16gmnIDA9ENZgN0INKzgolqTURxZZ7bfaMCgyBFo10I'
    api_secret = 'UMcmk6M0LwNntRBtE8n6VHW8B9Wk7dcKcLAP6BJjOGt7iiUZcYFN4mgI2hlVCHdy'
    client = Client(api_key, api_secret)
    client.API_URL = 'https://testnet.binance.vision/api'

    # Get Data from Binance API
    btc_price = client.get_symbol_ticker(symbol="BTCUSDT")
    ltc_price = client.get_symbol_ticker(symbol="LTCUSDT")
    return btc_price, ltc_price

def price_diff(hist):
    ret = []
    for i in range(len(hist[0])):
        ret.append(float(hist[0][i])-float(hist[1][i]) >= 0.0)
    return ret

def price_percent_diff(hist):
    ret = []
    for i in range(len(hist[0])):
        ret.append((float(hist[0][i])-float(hist[1][i])) / float(hist[0][i]))
    return ret


# Historical Data to train
def get_frame(label):
    timestamp = client._get_earliest_valid_timestamp(label, '1d')
    past = client.get_historical_klines(label, "1m", start_str=timestamp, limit=500)
    # Results will be of attribute ['dateTime', 'open', 'high', 'low', 'close', 'volume', 
    #                                  'closeTime', 'quoteAssetVolume', 'numberOfTrades', 
    #                                  'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore']
    opens = []
    closes = []
    for entry in past:
        opens.append(entry[1])
        closes.append(entry[4])
    return (opens, closes)

def get_history(filename):
    btc = get_frame("BTCUSDT")
    ltc = get_frame("LTCUSDT")

    btc_attr = price_diff(btc)
    ltc_attr = price_diff(ltc)
    btc_percent = price_percent_diff(btc)
    ltc_percent = price_percent_diff(ltc)

    toWrite = ''
    for i in range(len(btc_attr)):
        try:
            if (btc_attr[i] == ltc_attr[i]):
                if (btc_percent[i] >= ltc_percent[i]):
                    label = 'btc'
                else:
                    label = 'ltc'
            else:
                if (btc_attr[i]):
                    label = 'btc'
                else:
                    label = 'ltc'
            btc_change = 'up' if btc_attr[i] else 'down'
            ltc_change = 'up' if ltc_attr[i] else 'down'
            toWrite += btc_change+","+ltc_change+","+label+"\n"
        except:
            print("Timing data for BTC and LTC mismatch")

    f = open(filename, "w")
    f.write(toWrite)
    f.close()

if __name__ == '__main__':
    get_history()