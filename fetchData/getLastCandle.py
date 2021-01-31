import requests
import json
from comptIndicators import computeRSI, computeMomentum, computeMA, dFromMA


def fetchData(timeframe):
    cointype: str = "btc"
    timeframe: str = timeframe

    url = f'https://{cointype}.history.hxro.io/{timeframe}'

    #  Last 44 closes prices (we do not pick current one -> start -2)
    r = requests.get(url).json()
    last_cp = r['data'][-2: -46: -1]
    lastCpInc = r['data'][-2: -52: -1]

    for i, el in enumerate(last_cp):
        last_cp[i] = el.get('close')

    for i, el in enumerate(lastCpInc):
        lastCpInc[i] = el.get('close')

    lastCp = last_cp[0:30]
    lastCp = lastCp[::-1]

    return lastCp, computeRSI(last_cp[::-1]), computeMomentum(last_cp), dFromMA(last_cp, computeMA(last_cp))
