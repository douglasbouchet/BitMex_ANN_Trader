import requests
import json
from comptIndicators import computeRSI

cointype: str = "btc"
timeframe: str = "1d"

url = f'https://{cointype}.history.hxro.io/{timeframe}'

#  Last 44 closes prices (we do not pick current one -> start -2)
last_cp = requests.get(url).json()['data'][-2: -46: -1]


for i, el in enumerate(last_cp):
    last_cp[i] = el.get('close')

# index 0 represent close price of last full candle
computeRSI(last_cp[::-1])
# get last 30 + 14 close price, thus can recompute rsi, moving avg, momentum
# and save them in the data set (so cp old data set from bachelor project)
