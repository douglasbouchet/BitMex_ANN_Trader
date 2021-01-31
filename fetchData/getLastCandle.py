import requests
import json
from comptIndicators import computeRSI, computeMomentum, computeMA, dFromMA

cointype: str = "btc"
timeframe: str = "1d"

url = f'https://{cointype}.history.hxro.io/{timeframe}'

#  Last 44 closes prices (we do not pick current one -> start -2)
r = requests.get(url).json()
last_cp = r['data'][-2: -46: -1]
lastCpInc = r['data'][-2: -52: -1]

for i, el in enumerate(last_cp):
    last_cp[i] = el.get('close')

for i, el in enumerate(lastCpInc):
    lastCpInc[i] = el.get('close')

# index 0 represent close price of last full candle
computeRSI(last_cp[::-1])
# get last 30 + 14 close price, thus can recompute rsi, moving avg, momentum
# and save them in the data set (so cp old data set from bachelor project)

computeMomentum(last_cp)

computeMA(lastCpInc)

dFromMA(last_cp, computeMA(lastCpInc))
