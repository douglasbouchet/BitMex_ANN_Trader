import requests
import json
import datetime
from datetime import timedelta
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

    # print(len(last_cp))
    # print(lastCp[0:30])
    return lastCp, computeRSI(last_cp[::-1]), computeMomentum(last_cp), dFromMA(last_cp, computeMA(last_cp))


fetchData("1h")

#cur = datetime.datetime.now()
# current = datetime.datetime(
#    cur.year, cur.month, cur.day, cur.hour, (cur.minute // 60 * 60), 0)
#
#cointype: str = "btc"
#timeframe: str = "1h"
#
#url = f'https://{cointype}.history.hxro.io/{timeframe}'
#
#  Last 44 closes prices (we do not pick current one -> start -2)
#r = requests.get(url).json()
# print(r)
#last_cp = r['data'][::-1][1:]
# print(last_cp[0:10])
#j = current.hour % 4
# print(j)
# print(last_cp[0:10])
#last_cp = last_cp[j:]

# print(last_cp[0:10])

# while (current.hour % 4 != 0):
#    print(current.hour)
#    current = datetime.datetime(
#        cur.year, cur.month, cur.day, cur.hour - 1, cur.minute, 0)
