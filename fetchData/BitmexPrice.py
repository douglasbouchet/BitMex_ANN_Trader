import requests
import numpy as np
import datetime

url = 'https://www.bitmex.com/api/v1/trade?symbol=.BXBT&count=100&columns=price&reverse=true'

r = requests.get(url).json()
# We want to predict up to 4 hours: ->
# 1. we download all the 1 minutes tics to rebuild the last close price for 1 minute timeframe,
# then we build for 15 min, 1hour, 4 hour + (see if we add some other timeframes)

# worst case: 4 * 60 * 53  = 12720 -> 13 request (1000 each) for the 4 hour timeframe

js = 0*np.empty((1))

for i in range(0, 13):
    if (i != 12):
        url = 'https://www.bitmex.com/api/v1/trade?symbol=.BXBT&start=' + \
            str(i*1000) + '&count=1000&columns=price&reverse=true'
    else:
        url = 'https://www.bitmex.com/api/v1/trade?symbol=.BXBT&start=' + \
            str(i*1000) + '&count=720&columns=price&reverse=true'
    js = np.concatenate((js, requests.get(url).json()))

js = np.delete(js, 0)

for i, el in enumerate(js):
    js[i] = datetime.datetime.strptime(
        el['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ'), el['price']


def _15m_Candle(js):
    while js[0][0].minute % 15 != 0:
        js = np.delete(js, 0)
    arr = [0] * 849
    j = 0
    for i, el in enumerate(js):
        if el[0].minute % 15 == 0:
            arr[j] = el
            j += 1
    return arr[0:53]


def _1h_Candle(js):
    while js[0][0].minute % 60 != 0:
        js = np.delete(js, 0)
    arr = [0] * 213
    j = 0
    for i, el in enumerate(js):
        if el[0].minute % 60 == 0:
            arr[j] = el
            j += 1
    return arr[0:53]


def _2h_Candle(js):
    while js[0][0].minute % 60 != 0 or js[0][0].hour % 2 != 0:
        js = np.delete(js, 0)
    arr = [0] * 106
    j = 0
    for i, el in enumerate(js):
        if el[0].minute % 60 == 0 and el[0].hour % 2 == 0:
            arr[j] = el
            j += 1
    return arr[0:53]


def _4h_Candle(js):
    while js[0][0].minute % 60 != 0 or js[0][0].hour % 4 != 0:
        js = np.delete(js, 0)
    arr = [0] * 53
    j = 0
    for i, el in enumerate(js):
        if el[0].minute % 60 == 0 and el[0].hour % 4 == 0:
            arr[j] = el
            j += 1
    return arr[0:53]


js15m = _15m_Candle(js)
js1h = _1h_Candle(js)
js2h = _2h_Candle(js)
js4h = _4h_Candle(js)


# print(js15m)
# print(js1h)
# print(js2h)
print(js4h)
print(len(js4h))
