import requests
import json

cointype: str = "btc"
timeframe: str = "1d"

url = f'https://{cointype}.history.hxro.io/{timeframe}'

r = requests.get(url)

json_data = r.json()

print(json_data.get('data')[-1])  # -1 gives the value of the current candle
# pick -2, else impossible to pick a trade since we need some time to perform computation
print(json_data.get('data')[-2])
# we use which correspond to last FULL candle to compute the next one (delay 2 (à vérifier))


TODO
# get last 30 + 14 close price, thus can recompute rsi, moving avg, momentum
# and save them in the data set (so cp old data set from bachelor project)
